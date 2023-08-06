#include <torch/extension.h>
#include <vector>

template <typename scalar_t>
scalar_t GetEpochGradientAddition(
    int64_t node_id, int64_t child_id, int64_t leaf_count,
    const torch::TensorAccessor<scalar_t, 1> &heights,
    const torch::TensorAccessor<scalar_t, 1> &ratios,
    const torch::TensorAccessor<scalar_t, 1> &bounds,
    const torch::TensorAccessor<scalar_t, 1> &grad_ratios) {
  if (bounds[node_id] == bounds[child_id]) {
    return grad_ratios[child_id - leaf_count] * ratios[child_id - leaf_count] /
           ratios[node_id - leaf_count];
  } else {
    auto node_id_res = node_id - leaf_count;
    return grad_ratios[child_id - leaf_count] * ratios[child_id - leaf_count] /
           (heights[node_id_res] - bounds[child_id]) *
           (heights[node_id_res] - bounds[node_id]) / ratios[node_id_res];
  }
}

template <typename scalar_t>
void UpdateGradientUnWeightedLogDensity(
    torch::TensorAccessor<scalar_t, 1> &grad_ratios,
    const torch::TensorAccessor<scalar_t, 1> &grad_heights,
    const torch::TensorAccessor<scalar_t, 1> &ratios,
    const torch::TensorAccessor<scalar_t, 1> &heights,
    const torch::TensorAccessor<scalar_t, 1> &bounds,
    const torch::TensorAccessor<int64_t, 2> &post_indexing) {
  auto leaf_count = grad_heights.sizes()[0] + 1;
  auto dim_indexing = post_indexing.sizes()[0];
  // root not included
  for (int64_t i = 0; i < dim_indexing - 1; i++) {
    auto node_id = post_indexing[i][0];
    auto child0_id = post_indexing[i][1];
    auto child1_id = post_indexing[i][2];
    if (node_id >= leaf_count) {
      auto node_id_res = node_id - leaf_count;
      grad_ratios[node_id_res] += (heights[node_id_res] - bounds[node_id]) /
                                  ratios[node_id_res] *
                                  grad_heights[node_id_res];
      if (child0_id >= leaf_count) {
        grad_ratios[node_id_res] +=
            GetEpochGradientAddition(node_id, child0_id, leaf_count, heights,
                                     ratios, bounds, grad_ratios);
      }
      if (child1_id >= leaf_count) {
        grad_ratios[node_id_res] +=
            GetEpochGradientAddition(node_id, child1_id, leaf_count, heights,
                                     ratios, bounds, grad_ratios);
      }
    }
  }
}

template <typename scalar_t>
scalar_t UpdateHeightParameterGradientUnweightedLogDensity(
    const torch::TensorAccessor<scalar_t, 1> &grad_height,
    const torch::TensorAccessor<scalar_t, 1> &ratios,
    const torch::TensorAccessor<scalar_t, 1> &bounds,
    const torch::TensorAccessor<int64_t, 2> &pre_indexing) {
  auto leaf_count = grad_height.sizes()[0] + 1;
  auto dim_indexing = pre_indexing.sizes()[0];
  std::vector<scalar_t> multipliers(leaf_count - 1);
  multipliers[pre_indexing[0][0] - leaf_count] = 1.0;

  for (int64_t i = 0; i < dim_indexing; i++) {
    auto node_id = pre_indexing[i][0];
    auto child_id = pre_indexing[i][1];
    if (child_id >= leaf_count) {
      multipliers[child_id - leaf_count] =
          ratios[child_id - leaf_count] * multipliers[node_id - leaf_count];
    }
  }

  scalar_t grad_root = 0;
  for (int64_t i = 0; i < grad_height.sizes()[0]; i++) {
    grad_root += grad_height[i] * multipliers[i];
  }
  return grad_root;
}

template <typename scalar_t>
torch::Tensor NodeHeightTransformForward(torch::Tensor ratios,
                                         torch::Tensor bounds,
                                         torch::Tensor pre_indexing) {
  auto dim_indexing = pre_indexing.sizes()[0];
  auto dim = ratios.sizes()[0];
  auto taxa_count = dim + 1;
  torch::Tensor heights = torch::empty_like(ratios);
  torch::TensorAccessor<int64_t, 2> pre_indexing_a =
      pre_indexing.accessor<int64_t, 2>();
  auto ratios_a = ratios.accessor<scalar_t, 1>();
  auto bounds_a = bounds.accessor<scalar_t, 1>();
  auto heights_a = heights.accessor<scalar_t, 1>();
  heights_a[dim - 1] = ratios_a[dim - 1];
  for (auto i = 0; i < dim_indexing; i++) {
    auto parent_id = pre_indexing_a[i][0];
    auto node_id = pre_indexing_a[i][1];
    if (node_id >= taxa_count) {
      heights_a[node_id - taxa_count] =
          bounds_a[node_id] +
          ratios_a[node_id - taxa_count] *
              (heights_a[parent_id - taxa_count] - bounds_a[node_id]);
    }
  }

  return {heights};
}

template <typename scalar_t>
torch::Tensor
NodeHeightTransformBackward(torch::Tensor grad_heights, torch::Tensor ratios,
                            torch::Tensor heights, torch::Tensor bounds,
                            torch::Tensor pre_indexing,
                            torch::Tensor post_indexing) {
  auto grad_heights_acc = grad_heights.accessor<scalar_t, 1>();
  auto ratios_acc = ratios.accessor<scalar_t, 1>();
  auto heights_acc = heights.accessor<scalar_t, 1>();
  auto bounds_acc = bounds.accessor<scalar_t, 1>();
  auto pre_indexing_acc = pre_indexing.accessor<int64_t, 2>();
  auto post_indexing_acc = post_indexing.accessor<int64_t, 2>();
  torch::Tensor grad_ratios = torch::zeros_like(ratios);
  auto grad_ratios_acc = grad_ratios.accessor<scalar_t, 1>();
  UpdateGradientUnWeightedLogDensity(grad_ratios_acc, grad_heights_acc,
                                     ratios_acc, heights_acc, bounds_acc,
                                     post_indexing_acc);

  grad_ratios[grad_heights.sizes()[0] - 1] =
      UpdateHeightParameterGradientUnweightedLogDensity(
          grad_heights_acc, ratios_acc, bounds_acc, pre_indexing_acc);

  return grad_ratios;
}

template <typename scalar_t>
torch::Tensor LogAbsDetJacobian(torch::Tensor ratios, torch::Tensor heights,
                                torch::Tensor bounds,
                                torch::Tensor pre_indexing) {
  auto dim_indexing = pre_indexing.sizes()[0];
  auto dim = ratios.sizes()[0];
  auto taxa_count = dim + 1;
  auto pre_indexing_a = pre_indexing.accessor<int64_t, 2>();
  auto bounds_a = bounds.accessor<scalar_t, 1>();
  auto heights_a = heights.accessor<scalar_t, 1>();
  scalar_t log_jacobian = 0.0;
  for (auto i = 0; i < dim_indexing; i++) {
    auto parent_id = pre_indexing_a[i][0];
    auto node_id = pre_indexing_a[i][1];
    if (node_id >= taxa_count) {
      log_jacobian +=
          log(heights_a[parent_id - taxa_count] - bounds_a[node_id]);
    }
  }
  return torch::tensor(log_jacobian).type_as(ratios);
}

template <typename scalar_t>
torch::Tensor
LogAbsDetJacobianBackward(torch::Tensor grad_out, torch::Tensor ratios,
                          torch::Tensor heights, torch::Tensor bounds,
                          torch::Tensor pre_indexing,
                          torch::Tensor post_indexing) {
  auto dim = ratios.sizes()[0];
  auto pre_indexing_dim = pre_indexing.sizes()[0];
  auto taxa_count = dim + 1;
  auto ratios_acc = ratios.accessor<scalar_t, 1>();
  auto heights_acc = heights.accessor<scalar_t, 1>();
  auto bounds_acc = bounds.accessor<scalar_t, 1>();
  auto pre_indexing_acc = pre_indexing.accessor<int64_t, 2>();
  auto post_indexing_acc = post_indexing.accessor<int64_t, 2>();
  torch::Tensor log_time = torch::zeros_like(ratios);
  auto log_time_acc = log_time.accessor<scalar_t, 1>();
  for (auto i = 0; i < pre_indexing_dim; i++) {
    auto node_id = pre_indexing_acc[i][1];
    if (node_id >= taxa_count) {
      log_time_acc[node_id - taxa_count] =
          1.0 / (heights_acc[node_id - taxa_count] - bounds_acc[node_id]);
    }
  }
  torch::Tensor grad_ratios = torch::zeros_like(ratios);
  auto grad_ratios_acc = grad_ratios.accessor<scalar_t, 1>();
  UpdateGradientUnWeightedLogDensity(grad_ratios_acc, log_time_acc, ratios_acc,
                                     heights_acc, bounds_acc,
                                     post_indexing_acc);
  grad_ratios_acc[dim - 1] += UpdateHeightParameterGradientUnweightedLogDensity(
      log_time_acc, ratios_acc, bounds_acc, pre_indexing_acc);

  for (auto i = 0; i < pre_indexing_dim; i++) {
    auto node_id = pre_indexing_acc[i][1];
    if (node_id >= taxa_count) {
      grad_ratios_acc[node_id - taxa_count] -=
          1.0 / ratios_acc[node_id - taxa_count];
    }
  }
  return grad_ratios * grad_out;
}

PYBIND11_MODULE(tree_height_transform_cpp, m) {
  m.doc() =
      R"pbdoc(Module for converting ratio/root height to node height parameters.

  Efficient calculation of the ratio and root height gradient, adpated from BEAST.
  Xiang et al. Scalable Bayesian divergence time estimation with ratio transformation (2021).
  https://arxiv.org/abs/2110.13298
  )pbdoc";

  m.def("forward", &NodeHeightTransformForward<double>,
        "Node height transform forward");
  m.def("backward", &NodeHeightTransformBackward<double>,
        "Node height transform backward");

  m.def("log_abs_det_jacobian", &LogAbsDetJacobian<double>,
        "Log absolute determinant of Jacobian forward");
  m.def("log_abs_det_jacobian_backward", &LogAbsDetJacobianBackward<double>,
        "Log absolute determinant of Jacobian backward");
}
