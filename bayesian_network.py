from pgmpy.models import BayesianNetwork
from pgmpy.inference import VariableElimination
from pgmpy.factors.discrete import TabularCPD


def main():
  # define the model
  model = BayesianNetwork([('M', 'V'), ('F', 'V'), ('P', 'V'), ('S', 'V'), ('V', 'I'), ('I', 'B'), ('V', 'T')])

  # define the Conditional Probability Distributions (CPDs)
  # refer to the PDF to understand values
  cpd_m = TabularCPD(variable='M', variable_card=2, values=[[0.5],[0.5]]) # P(M)
  cpd_f = TabularCPD(variable='F', variable_card=2, values=[[0.3],[0.7]]) # P(F)
  cpd_p = TabularCPD(variable='P', variable_card=2, values=[[0.8],[0.2]]) # P(P)
  cpd_s = TabularCPD(variable='S', variable_card=2, values=[[0.9],[0.1]]) # P(S)
  cpd_v = TabularCPD(variable='V', variable_card=2, values=
      [[1,0.8,0.95,0.75,0.4,0.2,0.35,0.15,0.85,0.65,0.8,0.6,0.25,0.05,0.2,0],
      [0,0.2,0.05,0.25,0.6,0.8,0.65,0.85,0.15,0.35,0.2,0.4,0.75,0.95,0.8,1.0]],
      evidence=['M','F','P','S'], evidence_card=[2,2,2,2]) # P(V | M, F, P, S)
  cpd_i = TabularCPD(variable='I', variable_card=2, values=[[0.8,0.2],[0.2,0.8]], evidence=['V'], evidence_card=[2]) # P(I | V)
  cpd_b = TabularCPD(variable='B', variable_card=2, values=[[0.8,0.2],[0.2,0.8]], evidence=['I'], evidence_card=[2]) # P(B | I)
  cpd_t = TabularCPD(variable='T', variable_card=2, values=[[0.1,0.9],[0.9,0.1]], evidence=['V'], evidence_card=[2]) # P(T | V)
  
  # add the Conditional Probability Distributions to the model
  model.add_cpds(cpd_m, cpd_f, cpd_p, cpd_s, cpd_v, cpd_i, cpd_b, cpd_t)
  
  # check if the model is valid
  assert model.check_model(), "Model is incorrect"
  
  # create an inference object
  infer = VariableElimination(model)
  
  # compute utility values given all possible combinations of M, F, P, and S
  results = []
  for M in range(2):
    for F in range(2):
      for P in range(2):
        for S in range(2):
          T = infer.query(variables=['T'], evidence={'M': M, 'F': F, 'P': P, 'S': S}).values[1]
          I = infer.query(variables=['I'], evidence={'M': M, 'F': F, 'P': P, 'S': S}).values[1]
          B = infer.query(variables=['B'], evidence={'M': M, 'F': F, 'P': P, 'S': S}).values[1]
          utility = Result.compute_utility(T=T, I=I, B=B)
          results.append(Result(M=M, F=F, P=P, S=S, utility=utility))
  
  # order by best to worst options (depending on the utility)
  results.sort(reverse=True, key=lambda decision: decision.utility)
  Result.normalize(results)
  for result in results:
    print(result)

class Result:
  def __init__(self, M: float, F: float, P: float, S: float, utility: float):
    self.M = M
    self.F = F
    self.P = P
    self.S = S
    self.utility = utility
    
  def __str__(self):
    return str(self.utility) + " (M=" + str(self.M) + ", F=" + str(self.F) + ", P=" + str(self.P) + ", S=" + str(self.S) + ")"
    
  def compute_utility(T: float, I: float, B: float):
    # define utility weights
    T_WEIGHT = 0.55 # money for vacation
    I_WEIGHT = 0.6 # not infected
    B_WEIGHT = 0.8 # don't bite and infect family
  
    return T_WEIGHT * T + I_WEIGHT * I + B_WEIGHT * B
  
  def normalize(results: list):
    total = 0.0
    for result in results:
      total += result.utility
    for result in results:
      result.utility /= total


if __name__ == '__main__':
  main()
