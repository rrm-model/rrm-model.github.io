########################################
#
# @file LC_RUM_PRRM_muRRM_3classes.py
# @author: Sander van Cranenburgh, José Hernández & Gabriel Nova
# @date: 01/01/2024
#
#######################################
print("Start estimation of Latent Class RUM-muRRM-PRRM model (three classes)")
print(" ")

import pandas as pd
import biogeme.database as db
import biogeme.biogeme as bio
from biogeme.expressions import Beta, DefineVariable,Variable, log,exp,MonteCarlo,bioMax, bioMin, PanelLikelihoodTrajectory
import biogeme.models as models
import numpy as np

import warnings
warnings.filterwarnings('error')

# Load data
dat = pd.read_csv("Shopping_data_with_headers.dat",sep='\t')
database = db.Database("Shopping",dat)

database.panel("ID")

# Create variables FSG1 to FSG5
FSG1 = Variable('FSG1')
FSG2 = Variable('FSG2')
FSG3 = Variable('FSG3')
FSG4 = Variable('FSG4')
FSG5 = Variable('FSG5')

# Create variables FSO1 to FSO5
FSO1 = Variable('FSO1')
FSO2 = Variable('FSO2')
FSO3 = Variable('FSO3')
FSO4 = Variable('FSO4')
FSO5 = Variable('FSO5')

# Create variables TT1 to TT5
TT1 = Variable('TT1')
TT2 = Variable('TT2')
TT3 = Variable('TT3')
TT4 = Variable('TT4')
TT5 = Variable('TT5')

CHOICE = Variable('CHOICE')

# Define PRRM variables for RUM
FSG1_sc = database.DefineVariable('FSG1_sc', ( 1 / 1000 ) * FSG1 )
FSG2_sc = database.DefineVariable('FSG2_sc', ( 1 / 1000 ) * FSG2 )
FSG3_sc = database.DefineVariable('FSG3_sc', ( 1 / 1000 ) * FSG3 )
FSG4_sc = database.DefineVariable('FSG4_sc', ( 1 / 1000 ) * FSG4 )
FSG5_sc = database.DefineVariable('FSG5_sc', ( 1 / 1000 ) * FSG5 )

FSO1_sc = database.DefineVariable('FSO1_sc', ( 1 / 1000 ) * FSO1 )
FSO2_sc = database.DefineVariable('FSO2_sc', ( 1 / 1000 ) * FSO2 )
FSO3_sc = database.DefineVariable('FSO3_sc', ( 1 / 1000 ) * FSO3 )
FSO4_sc = database.DefineVariable('FSO4_sc', ( 1 / 1000 ) * FSO4 )
FSO5_sc = database.DefineVariable('FSO5_sc', ( 1 / 1000 ) * FSO5 )

TT1_sc = database.DefineVariable('TT1_sc', ( 1 / 100 ) * TT1 )
TT2_sc = database.DefineVariable('TT2_sc', ( 1 / 100 ) * TT2 )
TT3_sc = database.DefineVariable('TT3_sc', ( 1 / 100 ) * TT3 )
TT4_sc = database.DefineVariable('TT4_sc', ( 1 / 100 ) * TT4 )
TT5_sc = database.DefineVariable('TT5_sc', ( 1 / 100 ) * TT5 )



# Define PRRM variables for PRRM
X_FSG1 = database.DefineVariable('X_FSG1', ( bioMax( 0 , FSG2_sc - FSG1_sc ) + bioMax( 0 , FSG3_sc - FSG1_sc ) + bioMax( 0 , FSG4_sc - FSG1_sc ) + bioMax( 0 , FSG5_sc - FSG1_sc ) ))
X_FSG2 = database.DefineVariable('X_FSG2', ( bioMax( 0 , FSG1_sc - FSG2_sc ) + bioMax( 0 , FSG3_sc - FSG2_sc ) + bioMax( 0 , FSG4_sc - FSG2_sc ) + bioMax( 0 , FSG5_sc - FSG2_sc ) ))
X_FSG3 = database.DefineVariable('X_FSG3', ( bioMax( 0 , FSG1_sc - FSG3_sc ) + bioMax( 0 , FSG2_sc - FSG3_sc ) + bioMax( 0 , FSG4_sc - FSG3_sc ) + bioMax( 0 , FSG5_sc - FSG3_sc ) ))
X_FSG4 = database.DefineVariable('X_FSG4', ( bioMax( 0 , FSG1_sc - FSG4_sc ) + bioMax( 0 , FSG2_sc - FSG4_sc ) + bioMax( 0 , FSG3_sc - FSG4_sc ) + bioMax( 0 , FSG5_sc - FSG4_sc ) ))
X_FSG5 = database.DefineVariable('X_FSG5', ( bioMax( 0 , FSG1_sc - FSG5_sc ) + bioMax( 0 , FSG2_sc - FSG5_sc ) + bioMax( 0 , FSG3_sc - FSG5_sc ) + bioMax( 0 , FSG4_sc - FSG5_sc ) ))

X_FSO1 = database.DefineVariable('X_FSO1', ( bioMin( 0 , FSO2_sc - FSO1_sc ) + bioMin( 0 , FSO3_sc - FSO1_sc ) + bioMin( 0 , FSO4_sc - FSO1_sc ) + bioMin( 0 , FSO5_sc - FSO1_sc ) ))
X_FSO2 = database.DefineVariable('X_FSO2', ( bioMin( 0 , FSO1_sc - FSO2_sc ) + bioMin( 0 , FSO3_sc - FSO2_sc ) + bioMin( 0 , FSO4_sc - FSO2_sc ) + bioMin( 0 , FSO5_sc - FSO2_sc ) ))
X_FSO3 = database.DefineVariable('X_FSO3', ( bioMin( 0 , FSO1_sc - FSO3_sc ) + bioMin( 0 , FSO2_sc - FSO3_sc ) + bioMin( 0 , FSO4_sc - FSO3_sc ) + bioMin( 0 , FSO5_sc - FSO3_sc ) ))
X_FSO4 = database.DefineVariable('X_FSO4', ( bioMin( 0 , FSO1_sc - FSO4_sc ) + bioMin( 0 , FSO2_sc - FSO4_sc ) + bioMin( 0 , FSO3_sc - FSO4_sc ) + bioMin( 0 , FSO5_sc - FSO4_sc ) ))
X_FSO5 = database.DefineVariable('X_FSO5', ( bioMin( 0 , FSO1_sc - FSO5_sc ) + bioMin( 0 , FSO2_sc - FSO5_sc ) + bioMin( 0 , FSO3_sc - FSO5_sc ) + bioMin( 0 , FSO4_sc - FSO5_sc ) ))

X_TT1 = database.DefineVariable('X_TT1', ( bioMin( 0 , TT2_sc - TT1_sc ) + bioMin( 0 , TT3_sc - TT1_sc ) + bioMin( 0 , TT4_sc - TT1_sc ) + bioMin( 0 , TT5_sc - TT1_sc ) ))
X_TT2 = database.DefineVariable('X_TT2', ( bioMin( 0 , TT1_sc - TT2_sc ) + bioMin( 0 , TT3_sc - TT2_sc ) + bioMin( 0 , TT4_sc - TT2_sc ) + bioMin( 0 , TT5_sc - TT2_sc ) ))
X_TT3 = database.DefineVariable('X_TT3', ( bioMin( 0 , TT1_sc - TT3_sc ) + bioMin( 0 , TT2_sc - TT3_sc ) + bioMin( 0 , TT4_sc - TT3_sc ) + bioMin( 0 , TT5_sc - TT3_sc ) ))
X_TT4 = database.DefineVariable('X_TT4', ( bioMin( 0 , TT1_sc - TT4_sc ) + bioMin( 0 , TT2_sc - TT4_sc ) + bioMin( 0 , TT3_sc - TT4_sc ) + bioMin( 0 , TT5_sc - TT4_sc ) ))
X_TT5 = database.DefineVariable('X_TT5', ( bioMin( 0 , TT1_sc - TT5_sc ) + bioMin( 0 , TT2_sc - TT5_sc ) + bioMin( 0 , TT3_sc - TT5_sc ) + bioMin( 0 , TT4_sc - TT5_sc ) ))

# Define PRRM variables for muRRM
FSG2_1 = database.DefineVariable('FSG2_1', ( FSG2_sc - FSG1_sc )) 
FSG3_1 = database.DefineVariable('FSG3_1', ( FSG3_sc - FSG1_sc ))
FSG4_1 = database.DefineVariable('FSG4_1', ( FSG4_sc - FSG1_sc ))
FSG5_1 = database.DefineVariable('FSG5_1', ( FSG5_sc - FSG1_sc ))
FSG1_2 = database.DefineVariable('FSG1_2', ( FSG1_sc - FSG2_sc ))
FSG3_2 = database.DefineVariable('FSG3_2', ( FSG3_sc - FSG2_sc ))
FSG4_2 = database.DefineVariable('FSG4_2', ( FSG4_sc - FSG2_sc ))
FSG5_2 = database.DefineVariable('FSG5_2', ( FSG5_sc - FSG2_sc ))
FSG1_3 = database.DefineVariable('FSG1_3', ( FSG1_sc - FSG3_sc ))
FSG2_3 = database.DefineVariable('FSG2_3', ( FSG2_sc - FSG3_sc ))
FSG4_3 = database.DefineVariable('FSG4_3', ( FSG4_sc - FSG3_sc ))
FSG5_3 = database.DefineVariable('FSG5_3', ( FSG5_sc - FSG3_sc ))
FSG1_4 = database.DefineVariable('FSG1_4', ( FSG1_sc - FSG4_sc ))
FSG2_4 = database.DefineVariable('FSG2_4', ( FSG2_sc - FSG4_sc ))
FSG3_4 = database.DefineVariable('FSG3_4', ( FSG3_sc - FSG4_sc ))
FSG5_4 = database.DefineVariable('FSG5_4', ( FSG5_sc - FSG4_sc ))
FSG1_5 = database.DefineVariable('FSG1_5', ( FSG1_sc - FSG5_sc ))
FSG2_5 = database.DefineVariable('FSG2_5', ( FSG2_sc - FSG5_sc ))
FSG3_5 = database.DefineVariable('FSG3_5', ( FSG3_sc - FSG5_sc ))
FSG4_5 = database.DefineVariable('FSG4_5', ( FSG4_sc - FSG5_sc ))

FSO2_1 = database.DefineVariable('FSO2_1', ( FSO2_sc - FSO1_sc ))
FSO3_1 = database.DefineVariable('FSO3_1', ( FSO3_sc - FSO1_sc ))
FSO4_1 = database.DefineVariable('FSO4_1', ( FSO4_sc - FSO1_sc ))
FSO5_1 = database.DefineVariable('FSO5_1', ( FSO5_sc - FSO1_sc ))
FSO1_2 = database.DefineVariable('FSO1_2', ( FSO1_sc - FSO2_sc ))
FSO3_2 = database.DefineVariable('FSO3_2', ( FSO3_sc - FSO2_sc ))
FSO4_2 = database.DefineVariable('FSO4_2', ( FSO4_sc - FSO2_sc ))
FSO5_2 = database.DefineVariable('FSO5_2', ( FSO5_sc - FSO2_sc ))
FSO1_3 = database.DefineVariable('FSO1_3', ( FSO1_sc - FSO3_sc ))
FSO2_3 = database.DefineVariable('FSO2_3', ( FSO2_sc - FSO3_sc ))
FSO4_3 = database.DefineVariable('FSO4_3', ( FSO4_sc - FSO3_sc ))
FSO5_3 = database.DefineVariable('FSO5_3', ( FSO5_sc - FSO3_sc ))
FSO1_4 = database.DefineVariable('FSO1_4', ( FSO1_sc - FSO4_sc ))
FSO2_4 = database.DefineVariable('FSO2_4', ( FSO2_sc - FSO4_sc ))
FSO3_4 = database.DefineVariable('FSO3_4', ( FSO3_sc - FSO4_sc ))
FSO5_4 = database.DefineVariable('FSO5_4', ( FSO5_sc - FSO4_sc ))
FSO1_5 = database.DefineVariable('FSO1_5', ( FSO1_sc - FSO5_sc ))
FSO2_5 = database.DefineVariable('FSO2_5', ( FSO2_sc - FSO5_sc ))
FSO3_5 = database.DefineVariable('FSO3_5', ( FSO3_sc - FSO5_sc ))
FSO4_5 = database.DefineVariable('FSO4_5', ( FSO4_sc - FSO5_sc ))

TT2_1 = database.DefineVariable('TT2_1', ( TT2_sc - TT1_sc ))
TT3_1 = database.DefineVariable('TT3_1', ( TT3_sc - TT1_sc ))
TT4_1 = database.DefineVariable('TT4_1', ( TT4_sc - TT1_sc ))
TT5_1 = database.DefineVariable('TT5_1', ( TT5_sc - TT1_sc ))
TT1_2 = database.DefineVariable('TT1_2', ( TT1_sc - TT2_sc ))
TT3_2 = database.DefineVariable('TT3_2', ( TT3_sc - TT2_sc ))
TT4_2 = database.DefineVariable('TT4_2', ( TT4_sc - TT2_sc ))
TT5_2 = database.DefineVariable('TT5_2', ( TT5_sc - TT2_sc ))
TT1_3 = database.DefineVariable('TT1_3', ( TT1_sc - TT3_sc ))
TT2_3 = database.DefineVariable('TT2_3', ( TT2_sc - TT3_sc ))
TT4_3 = database.DefineVariable('TT4_3', ( TT4_sc - TT3_sc ))
TT5_3 = database.DefineVariable('TT5_3', ( TT5_sc - TT3_sc ))
TT1_4 = database.DefineVariable('TT1_4', ( TT1_sc - TT4_sc ))
TT2_4 = database.DefineVariable('TT2_4', ( TT2_sc - TT4_sc ))
TT3_4 = database.DefineVariable('TT3_4', ( TT3_sc - TT4_sc ))
TT5_4 = database.DefineVariable('TT5_4', ( TT5_sc - TT4_sc ))
TT1_5 = database.DefineVariable('TT1_5', ( TT1_sc - TT5_sc ))
TT2_5 = database.DefineVariable('TT2_5', ( TT2_sc - TT5_sc ))
TT3_5 = database.DefineVariable('TT3_5', ( TT3_sc - TT5_sc ))
TT4_5 = database.DefineVariable('TT4_5', ( TT4_sc - TT5_sc ))


# LC models get often stuck in local minima. Therefore, it is necessary to use a series of different starting values (SV) 
# Number of starting value sets
R = 10

# Number of parameters to be estimated (except classes and mu)
B = 9

# Set seed
np.random.seed(0)

# Generate random SV from an uniform distribution
minimum = -0.1
maximum = 0.1

startset = np.random.uniform(minimum,maximum,(R,B))

# Generate random SV for class parameter between 0 and 1
classset = np.random.rand(R,3)

# Generate random SV for mu parameters between 0 and mumax
mumax = 0.5
muset = np.random.uniform(0,mumax,(R,1))

# Start loop!
for r in range(0,R):

      #Parameters to be estimated
      # Arguments:
      #   - 1  Name for report; Typically, the same as the variable.
      #   - 2  Starting value.
      #   - 3  Lower bound.
      #   - 4  Upper bound.
      #   - 5  0: estimate the parameter, 1: keep it fixed.

      # Parameters: Note that latent class models often get stuck in local maxima. To ensure a global maximum multiple starting values should be tested.
      # To avoid getting trap in a local maxima, here we use starting values near the best known maximum.

      # Parameters Class 1 RUM
      B_FSG_1 = Beta('FSG_1',startset[r,0],-10,10,0)
      B_FSO_1 = Beta('FSO_1',startset[r,1],-10,10,0)
      B_TT_1  = Beta('TT_1',startset[r,2],-10,10,0)

      # Parameters Class 2 PRRM
      B_FSG_2 = Beta('FSG_2',startset[r,3],-10,10,0)
      B_FSO_2 = Beta('FSO_2',startset[r,4],-10,0,0)
      B_TT_2  = Beta('TT_2',startset[r,5],-10,10,0)

      # Parameters Class 3 muRRM
      B_FSG_3 = Beta('FSG_3',startset[r,6],-10,10,0)
      B_FSO_3 = Beta('FSO_3',startset[r,7],-10,10,0)
      B_TT_3  = Beta('TT_3',startset[r,8],-10,10,0)
      mu_3    = Beta('mu_3',muset[r,0],0.1,10,0)

      # Class membership parameters
      s1 = Beta('s1',classset[r,0],-100,100,1)
      s2 = Beta('s2',classset[r,1],-100,100,0)
      s3 = Beta('s3',classset[r,2],-100,100,0)

      # Utility / regret functions

      # RUM class 
      V1_1 = B_FSG_1 * FSG1_sc + B_FSO_1 * FSO1_sc + B_TT_1 * TT1_sc
      V2_1 = B_FSG_1 * FSG2_sc + B_FSO_1 * FSO2_sc + B_TT_1 * TT2_sc
      V3_1 = B_FSG_1 * FSG3_sc + B_FSO_1 * FSO3_sc + B_TT_1 * TT3_sc
      V4_1 = B_FSG_1 * FSG4_sc + B_FSO_1 * FSO4_sc + B_TT_1 * TT4_sc
      V5_1 = B_FSG_1 * FSG5_sc + B_FSO_1 * FSO5_sc + B_TT_1 * TT5_sc

      # PRRM Class
      R1_2 = B_FSG_2 * X_FSG1 + B_FSO_2 * X_FSO1 + B_TT_2 * X_TT1 
      R2_2 = B_FSG_2 * X_FSG2 + B_FSO_2 * X_FSO2 + B_TT_2 * X_TT2 
      R3_2 = B_FSG_2 * X_FSG3 + B_FSO_2 * X_FSO3 + B_TT_2 * X_TT3 
      R4_2 = B_FSG_2 * X_FSG4 + B_FSO_2 * X_FSO4 + B_TT_2 * X_TT4 
      R5_2 = B_FSG_2 * X_FSG5 + B_FSO_2 * X_FSO5 + B_TT_2 * X_TT5 

      # muRRM Class
      R1_3 = mu_3 * (                                                 log( 1 + exp( ( B_FSG_3 / mu_3 ) * FSG2_1 ) ) + log( 1 + exp( ( B_FSG_3 / mu_3 ) * FSG3_1 ) ) + log( 1 + exp( ( B_FSG_3 / mu_3 ) * FSG4_1 ) ) + log( 1 + exp( ( B_FSG_3 / mu_3 ) * FSG5_1 ) )                                                 + log( 1 + exp( ( B_FSO_3 / mu_3 ) * FSO2_1 ) ) + log( 1 + exp( ( B_FSO_3 / mu_3 ) * FSO3_1 ) ) + log( 1 + exp( ( B_FSO_3 / mu_3 ) * FSO4_1 ) ) + log( 1 + exp( ( B_FSO_3 / mu_3 ) * FSO5_1 ) )                                               + log( 1 + exp( ( B_TT_3 / mu_3 ) * TT2_1 ) ) + log( 1 + exp( ( B_TT_3 / mu_3 ) * TT3_1 ) ) + log( 1 + exp( ( B_TT_3 / mu_3 ) * TT4_1 ) ) + log( 1 + exp( ( B_TT_3 / mu_3 ) * TT5_1 ) ))
      R2_3 = mu_3 * ( log( 1 + exp( ( B_FSG_3 / mu_3 ) * FSG1_2 ) )                                                 + log( 1 + exp( ( B_FSG_3 / mu_3 ) * FSG3_2 ) ) + log( 1 + exp( ( B_FSG_3 / mu_3 ) * FSG4_2 ) ) + log( 1 + exp( ( B_FSG_3 / mu_3 ) * FSG5_2 ) ) + log( 1 + exp( ( B_FSO_3 / mu_3 ) * FSO1_2 ) )                                                 + log( 1 + exp( ( B_FSO_3 / mu_3 ) * FSO3_2 ) ) + log( 1 + exp( ( B_FSO_3 / mu_3 ) * FSO4_2 ) ) + log( 1 + exp( ( B_FSO_3 / mu_3 ) * FSO5_2 ) ) + log( 1 + exp( ( B_TT_3 / mu_3 ) * TT1_2 ) )                                               + log( 1 + exp( ( B_TT_3 / mu_3 ) * TT3_2 ) ) + log( 1 + exp( ( B_TT_3 / mu_3 ) * TT4_2 ) ) + log( 1 + exp( ( B_TT_3 / mu_3 ) * TT5_2 ) ))
      R3_3 = mu_3 * ( log( 1 + exp( ( B_FSG_3 / mu_3 ) * FSG1_3 ) ) + log( 1 + exp( ( B_FSG_3 / mu_3 ) * FSG2_3 ) )                                                 + log( 1 + exp( ( B_FSG_3 / mu_3 ) * FSG4_3 ) ) + log( 1 + exp( ( B_FSG_3 / mu_3 ) * FSG5_3 ) ) + log( 1 + exp( ( B_FSO_3 / mu_3 ) * FSO1_3 ) ) + log( 1 + exp( ( B_FSO_3 / mu_3 ) * FSO2_3 ) )                                                 + log( 1 + exp( ( B_FSO_3 / mu_3 ) * FSO4_3 ) ) + log( 1 + exp( ( B_FSO_3 / mu_3 ) * FSO5_3 ) ) + log( 1 + exp( ( B_TT_3 / mu_3 ) * TT1_3 ) ) + log( 1 + exp( ( B_TT_3 / mu_3 ) * TT2_3 ) )                                               + log( 1 + exp( ( B_TT_3 / mu_3 ) * TT4_3 ) ) + log( 1 + exp( ( B_TT_3 / mu_3 ) * TT5_3 ) ))
      R4_3 = mu_3 * ( log( 1 + exp( ( B_FSG_3 / mu_3 ) * FSG1_4 ) ) + log( 1 + exp( ( B_FSG_3 / mu_3 ) * FSG2_4 ) ) + log( 1 + exp( ( B_FSG_3 / mu_3 ) * FSG3_4 ) )                                                 + log( 1 + exp( ( B_FSG_3 / mu_3 ) * FSG5_4 ) ) + log( 1 + exp( ( B_FSO_3 / mu_3 ) * FSO1_4 ) ) + log( 1 + exp( ( B_FSO_3 / mu_3 ) * FSO2_4 ) ) + log( 1 + exp( ( B_FSO_3 / mu_3 ) * FSO3_4 ) )                                                 + log( 1 + exp( ( B_FSO_3 / mu_3 ) * FSO5_4 ) ) + log( 1 + exp( ( B_TT_3 / mu_3 ) * TT1_4 ) ) + log( 1 + exp( ( B_TT_3 / mu_3 ) * TT2_4 ) ) + log( 1 + exp( ( B_TT_3 / mu_3 ) * TT3_4 ) )                                               + log( 1 + exp( ( B_TT_3 / mu_3 ) * TT5_4 ) ))
      R5_3 = mu_3 * ( log( 1 + exp( ( B_FSG_3 / mu_3 ) * FSG1_5 ) ) + log( 1 + exp( ( B_FSG_3 / mu_3 ) * FSG2_5 ) ) + log( 1 + exp( ( B_FSG_3 / mu_3 ) * FSG3_5 ) ) + log( 1 + exp( ( B_FSG_3 / mu_3 ) * FSG4_5 ) )                                                 + log( 1 + exp( ( B_FSO_3 / mu_3 ) * FSO1_5 ) ) + log( 1 + exp( ( B_FSO_3 / mu_3 ) * FSO2_5 ) ) + log( 1 + exp( ( B_FSO_3 / mu_3 ) * FSO3_5 ) ) + log( 1 + exp( ( B_FSO_3 / mu_3 ) * FSO4_5 ) )                                                 + log( 1 + exp( ( B_TT_3 / mu_3 ) * TT1_5 ) ) + log( 1 + exp( ( B_TT_3 / mu_3 ) * TT2_5 ) ) + log( 1 + exp( ( B_TT_3 / mu_3 ) * TT3_5 ) ) + log( 1 + exp( ( B_TT_3 / mu_3 ) * TT4_5 ) )                                              )



      # Associate utility functions with the numbering of alternatives
      V1 = {1: V1_1,
      2: V2_1,
      3: V3_1,
      4: V4_1,
      5: V5_1}

      V2 = {1: -R1_2,
      2: -R2_2,
      3: -R3_2,
      4: -R4_2,
      5: -R5_2}

      V3 = {1: -R1_3,
      2: -R2_3,
      3: -R3_3,
      4: -R4_3,
      5: -R5_3}

      # Associate the availability conditions with the alternatives
      one =1
      av = {1: one,
            2: one,
            3: one,
            4: one,
            5: one}

      # Class membership model
      probClass1 = exp(s1)/(exp(s1) + exp(s2) + exp(s3))
      probClass2 = exp(s2)/(exp(s1) + exp(s2) + exp(s3))
      probClass3 = exp(s3)/(exp(s1) + exp(s2) + exp(s3))

      # The choice model is a logit, with availability conditions
      prob1 = models.logit(V1,av,CHOICE)
      prob2 = models.logit(V2,av,CHOICE)
      prob3 = models.logit(V3,av,CHOICE)

      #Conditional probability for the sequence of choices of an individual
      ProbIndiv_1 = PanelLikelihoodTrajectory(prob1)
      ProbIndiv_2 = PanelLikelihoodTrajectory(prob2)
      ProbIndiv_3 = PanelLikelihoodTrajectory(prob3)

      # Define the likelihood function for the estimation
      biogeme = bio.BIOGEME(database,log(probClass1 * ProbIndiv_1 + probClass2 * ProbIndiv_2 + probClass3 * ProbIndiv_3))

      # Name biogeme object to identify each repetition
      biogeme.modelName = "LC3_RUM-PRRM-muRRM_rep_" + str(r+1)

      # Estimate!
      # It is possible that starting values are infeasible. The following condition allows to skip errors.
      try:
            results = biogeme.estimate()
            print("Starting value set " + str(r+1) + "/   LL: " + str(results.getGeneralStatistics()['Final log likelihood'][0]))
      except:
            print("Starting value set " + str(r+1) + "/   Convergence Error")


print(" ")
print("Estimations completed")
print("Open the estimation results for the model with the highest LL")
