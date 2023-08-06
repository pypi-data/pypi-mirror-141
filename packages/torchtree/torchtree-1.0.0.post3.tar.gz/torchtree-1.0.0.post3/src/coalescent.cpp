#include <algorithm> // std::sort, std::stable_sort
#include <numeric>   // std::iota
#include <torch/extension.h>
#include <vector>

using namespace torch::indexing;

// heights is one dimensional
double calculate_constant(torch::Tensor& heights,
                          double theta, torch::Tensor &indexes) {
  int64_t node_count = indexes.size(0);
  int64_t taxa_count = (node_count + 1) / 2;
  double logP = -std::log(theta) * static_cast<double>(taxa_count - 1);
  double lineages = 1.0;
  torch::TensorAccessor<double, 1> heights_a = heights.accessor<double, 1>();
  torch::TensorAccessor<int64_t, 1> indexes_a = indexes.accessor<int64_t, 1>();

  for (int64_t i = 0; i < node_count - 1; i++) {
    double interval = heights_a[indexes_a[i + 1]] - heights_a[indexes_a[i]];
    double lambda = (lineages * (lineages - 1.0) / 2.0) / theta;
    logP -= lambda * interval;

    if (indexes_a[i + 1] >= taxa_count) {
      lineages--;
    } else {
      lineages++;
    }
  }
  return logP;
}

double calculate_constant_theta_grad(torch::Tensor &heights,
                                     double theta,
                                     torch::Tensor &indexes) {
  int64_t node_count = indexes.size(0);
  int64_t taxa_count = (node_count + 1) / 2;
  double dlogP = -(static_cast<double>(taxa_count) - 1.0) / theta;
  double lineages = 1.0;
  double theta2 = theta * theta;
  torch::TensorAccessor<double, 1> heights_a = heights.accessor<double, 1>();
  torch::TensorAccessor<int64_t, 1> indexes_a = indexes.accessor<int64_t, 1>();

  for (size_t i = 0; i < node_count - 1; i++) {
    double interval = heights_a[indexes_a[i + 1]] - heights_a[indexes_a[i]];
    dlogP += (lineages * (lineages - 1.0) / 2.0) * interval / theta2;

    if (indexes_a[i + 1] >= taxa_count) {
      lineages--;
    } else {
      lineages++;
    }
  }
  return dlogP;
}

torch::Tensor
calculate_constant_heights_grad(double theta, torch::Tensor &indexes) {
  int64_t node_count = indexes.size(0);
  int64_t taxa_count = (node_count + 1) / 2;
  double lineages = 1.0;
  std::vector<double> height_grad(taxa_count - 1);
  std::vector<double> interval_grad(node_count - 1);
  torch::TensorAccessor<int64_t, 1> indexes_a = indexes.accessor<int64_t, 1>();

  for (int64_t i = 0; i < node_count - 1; i++) {
    interval_grad[i] = -(lineages * (lineages - 1.0) / 2.0) / theta;
    if (indexes_a[i + 1] >= taxa_count) {
      lineages--;
    } else {
      lineages++;
    }
    // std::cout <<  interval_grad[i] <<std::endl;
  }

  for (size_t i = 0; i < node_count - 2; i++) {
    if (indexes_a[i + 1] >= taxa_count) {
      height_grad[indexes_a[i + 1] - taxa_count] += interval_grad[i];
      height_grad[indexes_a[i + 1] - taxa_count] -= interval_grad[i + 1];
    }
  }
  height_grad[taxa_count - 2] += interval_grad[node_count - 2];

  return torch::tensor(height_grad);
}

// sampling_times [N]
// heights [B,2N-1] or [2N-1] if heights is data
// theta [B]
std::vector<torch::Tensor> constant_forward(torch::Tensor sampling_times,
                               torch::Tensor heights, torch::Tensor theta) {
  int64_t taxa_count = sampling_times.size(0);
  int64_t node_count = taxa_count * 2 - 1;
  int64_t batch_dim = theta.size(0);

  torch::Tensor logP = torch::empty(batch_dim, theta.dtype());
  torch::Tensor all_indexes = torch::empty({batch_dim, node_count},
                                   torch::TensorOptions().dtype(torch::kInt64));

  for (int64_t batch_idx = 0; batch_idx < batch_dim; batch_idx++) {
//    std::vector<size_t> indexes(node_count);
    auto heights1 =
        heights.dim() == 1 ? heights : heights.index({batch_idx, "..."});
    torch::Tensor all_heights = torch::cat({sampling_times, heights1});
    auto indexes = all_heights.argsort();
//    iota(indexes.begin(), indexes.end(), 0);
//    stable_sort(indexes.begin(), indexes.end(),
//                [&all_heights_a](size_t i1, size_t i2) {
//                  return all_heights_a[i1] < all_heights_a[i2];
//                });

    logP[batch_idx] = calculate_constant(
        all_heights, theta[batch_idx].item<double>(), indexes);
      all_indexes[batch_idx] = indexes;
  }
  return {logP, all_indexes};
}

std::vector<torch::Tensor> constant_backward(torch::Tensor indexes,
torch::Tensor sampling_times,
                                             torch::Tensor heights,
                                             torch::Tensor theta) {
  int64_t taxa_count = sampling_times.size(0);
  int64_t node_count = taxa_count * 2 - 1;
  int64_t batch_dim = theta.size(0);

  auto options = torch::TensorOptions().dtype(torch::kFloat64);
  torch::Tensor theta_grad = torch::empty({batch_dim, 1}, options);
  torch::Tensor heights_grad =
      torch::empty({batch_dim, taxa_count - 1}, options);

  for (int64_t batch_idx = 0; batch_idx < batch_dim; batch_idx++) {
//    std::vector<size_t> indexes(node_count);
    auto heights1 =
        heights.dim() == 1 ? heights : heights.index({batch_idx, "..."});
    torch::Tensor all_heights = torch::cat({sampling_times, heights1});
//    torch::TensorAccessor<double, 1> all_heights_a =
//        all_heights.accessor<double, 1>();
//    iota(indexes.begin(), indexes.end(), 0);
//    stable_sort(indexes.begin(), indexes.end(),
//                [&all_heights_a](size_t i1, size_t i2) {
//                  return all_heights_a[i1] < all_heights_a[i2];
//                });

    double thetaDouble = theta.index({batch_idx, "..."}).item<double>();
    auto idxes = indexes.index({batch_idx});
    theta_grad.index_put_(
        {batch_idx, "..."},
        calculate_constant_theta_grad(all_heights, thetaDouble, idxes));

    if (heights.requires_grad()) {
      heights_grad.index_put_(
          {batch_idx, "..."},
          calculate_constant_heights_grad(thetaDouble, idxes));
    }
  }
  return {heights_grad, theta_grad};
}

PYBIND11_MODULE(coalescent_cpp, m) {
  m.def("forward", &constant_forward, "constant coalescent forward");
  m.def("backward", &constant_backward, "constant coalescent backward");
}