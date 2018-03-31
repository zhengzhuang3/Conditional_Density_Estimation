import unittest
import warnings
import scipy.stats as stats
import numpy as np
from cde.evaluation.GoodnessOfFit import GoodnessOfFit, _multidim_cauchy_pdf
from cde.tests.Dummies import GaussianDummy, SimulationDummy

alpha = 0.05

class TestGoodnessOfFitTests(unittest.TestCase):

  """ --- plausibility checks with dummy (gaussian) estimators and simulators --- """

  # def test_gaussian_dummy_kolmogorov_cdf_1(self):
  #   est = GaussianDummy(mean=2, ndim_x=1, ndim_y=1)
  #   prob_model = SimulationDummy(mean=2, ndim_x=1, ndim_y=1)
  #   gof = GoodnessOfFit(est, prob_model, n_observations=10000)
  #   gof_results = gof.compute_results()
  #   print("cdf-based KS test (t, p): ", gof_results.mean_ks_stat, gof_results.mean_ks_pval, "alpha: ", alpha)
  #   print(gof)
  #   self.assertGreater(gof_results.mean_ks_pval, alpha)
  #   self.assertLess(gof_results.kl_divergence, 0.01)
  #
  #
  # def test_gaussian_dummy_kolmogorov_cdf_2(self):
  #   est = GaussianDummy(mean=2)
  #   prob_model = SimulationDummy(mean=6)
  #   gof = GoodnessOfFit(est, prob_model, n_observations=10000)
  #   gof_results = gof.compute_results()
  #   print("cdf-based KS test (t, p): ", gof_results.mean_ks_stat, gof_results.mean_ks_pval, "alpha: ", alpha)
  #   print(gof)
  #   self.assertLess(gof_results.mean_ks_pval, alpha)
  #
  #
  # def test_gaussian_dummy_kl_divergence1(self):
  #   est = GaussianDummy(mean=2)
  #   prob_model = SimulationDummy(mean=2)
  #   gof = GoodnessOfFit(est, prob_model, n_observations=10000)
  #   kl = gof.kl_divergence()
  #   print("KL-Divergence:", kl)
  #   self.assertLess(kl, 0.2)
  #
  # def test_gaussian_dummy_kl_divergence(self):
  #   est = GaussianDummy(mean=2)
  #   prob_model = SimulationDummy(mean=4)
  #   gof = GoodnessOfFit(est, prob_model, n_observations=10000)
  #   gof_results = gof.compute_results()
  #   print("KL-Divergence:", gof_results.kl_divergence)
  #   print(gof)
  #   self.assertGreater(gof_results.kl_divergence, 0.01)
  #
  # def test_gaussian_dummy_kl_divergence2(self):
  #   est = GaussianDummy(mean=2)
  #   prob_model1 = SimulationDummy(mean=4)
  #   gof1 = GoodnessOfFit(est, prob_model1, n_observations=10000)
  #   gof_results1 = gof1.compute_results()
  #
  #   prob_model2 = SimulationDummy(mean=3)
  #   gof2 = GoodnessOfFit(est, prob_model2, n_observations=10000)
  #   gof_results2 = gof2.compute_results()
  #   self.assertLess(gof_results2.kl_divergence, gof_results1.kl_divergence)

  def test_gaussian_dummy_hellinger_distance_mc(self):
    mu1 = np.array([0, 0])
    mu2 = np.array([0, 0])
    sigma1 = np.identity(n=2)*2
    sigma2 = np.identity(n=2)*1

    # Analytical form Hellinger Distance
    hd_squared_analytic_result = np.sqrt(1 - (2**0.5 / 1.5))

    x = np.asarray([[0, 0], [1,1]])

    est = GaussianDummy(mean=mu1, cov=sigma1, ndim_x=2, ndim_y=2)
    prob_model1 = SimulationDummy(mean=mu2, cov=sigma2, ndim_x=2, ndim_y=2)

    gof1 = GoodnessOfFit(est, prob_model1, n_observations=10000)
    self.assertAlmostEqual(hd_squared_analytic_result, gof1.hellinger_distance_mc(x_cond=x)[0], places=2)
    self.assertAlmostEqual(hd_squared_analytic_result, gof1.hellinger_distance_mc(x_cond=x)[1], places=2)

  def test_gaussian_dummy_kl_divergence_mc(self):
    mu1 = np.array([0, 0])
    mu2 = np.array([0, 0])
    sigma1 = np.identity(n=2) * 2
    sigma2 = np.identity(n=2) * 1

    # Analytical form Hellinger Distance
    kl_divergence_analytical = 0.5 * (1 - 2 + np.log(4))

    x = np.asarray([[0, 0], [1, 1]])

    est = GaussianDummy(mean=mu1, cov=sigma1, ndim_x=2, ndim_y=2)
    prob_model1 = SimulationDummy(mean=mu2, cov=sigma2, ndim_x=2, ndim_y=2)

    gof1 = GoodnessOfFit(est, prob_model1, n_observations=10000)
    self.assertAlmostEqual(kl_divergence_analytical, gof1.kl_divergence_mc(x_cond=x)[0], places=2)
    self.assertAlmostEqual(kl_divergence_analytical, gof1.kl_divergence_mc(x_cond=x)[1], places=2)

  def test_gaussian_dummy_js_divergence_mc(self):
    mu1 = np.array([0, 0])
    mu2 = np.array([0, 0])
    sigma1 = np.identity(n=2) * 2
    sigma2 = np.identity(n=2) * 1

    x = np.asarray([[0, 0], [1, 1]])

    est = GaussianDummy(mean=mu1, cov=sigma1, ndim_x=2, ndim_y=2)
    prob_model1 = SimulationDummy(mean=mu2, cov=sigma2, ndim_x=2, ndim_y=2)

    gof1 = GoodnessOfFit(est, prob_model1, n_observations=10000)
    self.assertGreaterEqual(1, gof1.js_divergence_mc(x_cond=x)[0])
    self.assertLessEqual(0, gof1.js_divergence_mc(x_cond=x)[0])

  def test_gaussian_dummy_wasserstein_distance_mc(self):
    mu1 = np.array([0, 0])
    mu2 = np.array([0, 0])
    sigma1 = np.identity(n=2) * 2
    sigma2 = np.identity(n=2) * 1

    # Analytical form upper bound of wassersetin distance
    wasserstein_upper = np.trace(sigma1 + sigma2 - 2*(np.linalg.cholesky(sigma1.dot(sigma2))))

    x = np.asarray([[0, 0], [1, 1]])

    est = GaussianDummy(mean=mu1, cov=sigma1, ndim_x=2, ndim_y=2)
    prob_model1 = SimulationDummy(mean=mu2, cov=sigma2, ndim_x=2, ndim_y=2)

    gof1 = GoodnessOfFit(est, prob_model1, n_observations=10000)
    wasserstein_dist_mc = gof1.wasserstein_distance_mc(x_cond=x)[0]
    print(wasserstein_dist_mc)
    self.assertGreaterEqual(wasserstein_upper, wasserstein_dist_mc)
    self.assertLessEqual(0, wasserstein_dist_mc)

  def test_multidim_chauchy(self):
    x1 = np.asarray([[1, 0], [0, 1]])
    x2 = np.asarray([[1]])

    self.assertEqual(_multidim_cauchy_pdf(x1)[0], _multidim_cauchy_pdf(x1)[1])
    self.assertAlmostEqual(_multidim_cauchy_pdf(x2, scale=4)[0], stats.cauchy.pdf(x2[0], scale=4)[0])

  def test_mc_intrgration_chauchy_1(self):
    mu1 = np.array([0])
    mu2 = np.array([0])
    sigma1 = np.identity(n=1) * 2
    sigma2 = np.identity(n=1) * 1

    est = GaussianDummy(mean=mu1, cov=sigma1, ndim_x=1, ndim_y=1)
    prob_model1 = SimulationDummy(mean=mu2, cov=sigma2, ndim_x=1, ndim_y=1)

    gof1 = GoodnessOfFit(est, prob_model1, n_observations=10000)

    func = lambda y, x: stats.uniform.pdf(y, loc=-1, scale=2)
    x_cond = np.asarray([[0]])
    integral = gof1._mc_integration_cauchy(func, x_cond, n_samples=10 ** 5, batch_size=10 ** 4)
    self.assertAlmostEqual(1.0, integral[0], places=2)

  def test_mc_intrgration_chauchy_2(self):
    mu1 = np.array([0, 0])
    mu2 = np.array([0, 0])
    sigma1 = np.identity(n=2) * 2
    sigma2 = np.identity(n=2) * 1

    est = GaussianDummy(mean=mu1, cov=sigma1, ndim_x=2, ndim_y=2)
    prob_model1 = SimulationDummy(mean=mu2, cov=sigma2, ndim_x=2, ndim_y=2)

    gof1 = GoodnessOfFit(est, prob_model1, n_observations=10000)

    func = lambda y, x: stats.multivariate_normal.pdf(y, mean=[0,0], cov=np.diag([2,2]))
    x_cond = np.asarray([[0,0]])
    integral = gof1._mc_integration_cauchy(func, x_cond, n_samples=10 ** 5, batch_size=10 ** 4)
    self.assertAlmostEqual(1.0, integral[0], places=2)


if __name__ == '__main__':
  #pytest.main('--html=unittest_report.html --self-contained-html')
  if __name__ == '__main__':
    warnings.filterwarnings("ignore")


    testmodules = [
      'unittests_evaluations.TestGoodnessOfFitTests'
                   ]
    suite = unittest.TestSuite()
    for t in testmodules:
      try:
        # If the module defines a suite() function, call it to get the suite.
        mod = __import__(t, globals(), locals(), ['suite'])
        suitefn = getattr(mod, 'suite')
        suite.addTest(suitefn())
      except (ImportError, AttributeError):
        # else, just load all the test cases from the module.
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

    unittest.TextTestRunner().run(suite)