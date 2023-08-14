import ccnlab.benchmarks.classical as classical
import ccnnlab.evaluation as evaluation 

# choose which esp to run, filer by name (whats glob syntax)
for exp in classical.registry('*'):
    # esp often have multiple groups, each shown diff stimuli
	for g, group in exp.stimuli.items():
		# users free to decide how to init models & how many instances to allocate per group 
		for instance in range(N):
			model = YourModelHere() # not sure what this means by "model"

			# each group is shown a seq of trials, at eat htimestep the model input has a cs, ctx, and us
			# cs = cond. stimuli; ctx = context; us = uncond. stimuli
			# model output is a response value 
			for i, trial in enumerate(group):
				for t, timestep in enumerate(trial):
					cs, ctx, us = timestep
					response = model.act(cs, ctx, us) 
					exp.data[g][i][t]['response'].append(response)
					# what exactly are g, i, and t?? 
	# simulation results can be compared to empirical results from published work using eval metrics (quant) and plots (qual)
	empirical = exp.empirical_results
	simulated = exp.simulated_results()
	score = evaluation.correlation(empirical, simulated)
	plot()

# cs is a list of active stimuli (string ids) & their magnitudes (+, real val) -> most exp, the mag is 0 or 1
# ctx is the active context (string id); remains same throughout a trial
# us is the unconditioned stimuli magnitude (+, real val) -> most exp, either 0 or 1

# alternatively, cs and ctx can be one-hot vectors w/ dimensions equal to the stimuli and context space, respectively 
# at each timestep, the model should provide a response value (real val) indicating the strenth of the CR (cond. response)


# API 
import pandas as pd
import ccnlab.benchmarks.classical.core as cc 

@cc.registry.register # review what this is 
class Acquisition_ContinuousVsPartial(cc.ClassicalConditioningExperiment):
	def __init__(self, n=64, prob=0.6):
		# spec stimuli structure for each experimental group using abstract syntax
		super().__init__({
			'continous': cc.seq(
				cc.trial('A+'),
				repeat=n, name='train',
			),
			'partial': cc.seq(
				cc.sample({ cc.trial('A+'): prob, cc.trial('A-'): 1-prob }),
				repeat=n, name='train',
			)
		})
		# encode empirical results & configure plotting
		self.empirical_results = pd.DataFrame(
			columns = ['group', 'session', 'A'],
			data = [ ... ] # review PD syntax and what this means
		) 
		self.plots = [ lambda df, ax: cc.plot_lines(df, ax=ax, x='session') ] # what is the lambda doing here??? 

	# transform raw model respones to the same format as empirical results 
	def simulated_results(self):
		df = self.dataframe(lambda x: {
			'A': cc.conditioned_response(x['timesteps'], x['response'], ['A']),
		})
		return cc.trials_to_sessions(df, self.trials_per_session)

# what are all these CC stuff
# trials vs. whatnot 

# each experiment is a schedule of stimuli consisting of multiple trials per gruop 
# make a seuqence of notes -> abstract syntax tree 

	# STIMULUS -> leaf node specifying the presentation of a stimulus (string), its magnitude (Float), and its start & end timesteps in a trial (ints)
	# TRIALS -> compound node spec a trial consisting of the CS (list of `stimulus`), CTX (string), and US (`stimulus`)
	# SAMPLE -> compound node spec probabilities w/ which to choose each of its children
	# SEQUENCE -> compound node spec a sequence of nmodes, how many times to repeat the sequence, and a name (naming diff phases of)
