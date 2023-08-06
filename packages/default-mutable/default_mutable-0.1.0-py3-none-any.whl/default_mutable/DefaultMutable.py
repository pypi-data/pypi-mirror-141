from functools import wraps
import inspect

def defaultMutable(*default_empty, **default_set):
	
	set_all_default = False
	
	def factory(func):
		
		@wraps(func)
		def wrapper(*args, **kwargs):
	
			# Getting the specifications of the function
			spec = inspect.getfullargspec(func)

			# Rewrite the default value for the lists in order to prevent mutable unexpected behavior
			default_mutable_values = {}
			if spec.defaults is not None:
				
				# Reversing the argument list as the arguments with default value are at the end
				spec_args = spec.args[::-1]
				for idx, default_value in enumerate(spec.defaults[::-1]):
					
					# Checking if the default value of the argument is preset
					if spec_args[idx] in default_set and isinstance(default_value, (list, dict)):
						if isinstance(default_set[spec_args[idx]], (list, dict)) == False:
							raise Exception(f'defaultMutable error: Argument "{spec_args[idx]}" has type "{type(spec_args[idx])}"; expected "{type(default_value)}"')
							
						default_mutable_values[spec_args[idx]] = default_set[spec_args[idx]].copy()
						
					# create empty list
					elif isinstance(default_value, list) and (set_all_default == True or spec_args[idx] in default_empty):
						default_mutable_values[spec_args[idx]] = []
					
					# Create empty dictionary
					elif isinstance(default_value, dict) and (set_all_default == True or spec_args[idx] in default_empty):
						default_mutable_values[spec_args[idx]] = {}
				
				# Removing the default mutable values if they are in the "args" list to avoid overriding the passed value
				len_args = len(args)
				for idx, spec_arg in enumerate(spec.args):
					if idx <= len_args - 1 and spec_arg in default_mutable_values:
						del default_mutable_values[spec_arg]
					elif idx >= len_args:
						break
			
			# We do not need to remove the default mutable values if they are in "kwargs", it is taken care of automatically next
			if len(default_mutable_values) > 0:
				kwargs = {
					**default_mutable_values,
					**kwargs,
				}
				
			# Executing the function with the decorator
			return func(*args, **kwargs)
			
		return wrapper
	
	# In case the decorator was not executed, we assume all the default values are empty dictionaries and lists
	if len(default_empty) == 1 and callable(default_empty[0]) and len(default_set) == 0:
		set_all_default = True
		return factory(default_empty[0])
	
	else:
		return factory