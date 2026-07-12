import Chromify
Chromify.init() # Run to import gradient(...)


RED 	=	Chromify.Color(	255, 	0, 		0	)
GREEN	= 	Chromify.Color(	0, 		255, 	0	)
BLUE 	= 	Chromify.Color(	0, 		0, 		255	)
WHITE	= 	Chromify.Color(	255,	255,	255	)

PASS_TEXT = Chromify.Fore.color(GREEN) + "Test Passed! ✅" + Chromify.Fore.color(WHITE)
FAILED_TEXT = Chromify.Fore.color(RED) + "Test Failed! ❌" + Chromify.Fore.color(WHITE)


def todo(msg="Hit incomplete code"):
	raise Todo(msg)

# Create an exception for an incomplete code section
# Inherit from the default exception class so that tracebacks are handled by the built in class, saving workload.
class Todo(Exception):
	# Initiate the super constructor of the class that this object inherits from so it initiates properly with the necessary functions
	def __init__(self, msg):
		self.msg = msg
		super().__init__(self.msg)
	# Overload the method that converts the class to a string for custom messages in the terminal.
	def __str__(self):
		return Chromify.gradient(RED, BLUE, self.msg + "!!!")

class AssertEqFailed(Exception):
	def __init__(self, lhs, rhs):
		self.lhs = lhs
		self.rhs = rhs
		super().__init__()
	def __str__(self):
		return Chromify.Fore.color(RED) + "Values LHS and RHS are not equal" + Chromify.Fore.color(BLUE) + f"\n{self.lhs}" + Chromify.Fore.color(RED) + " != " + Chromify.Fore.color(BLUE) + f"{self.rhs}" + Chromify.Fore.color(WHITE)
	
class Ok: pass

def assert_eq(lhs, rhs) -> AssertEqFailed | Ok:
	if lhs != rhs:
		return AssertEqFailed(lhs, rhs)
	return Ok

def test_errors(func, test_data: list, raise_error=True):
	# Store the count of passed and failed tests for later viewing to review the function.
	tests_passed = 0
	tests_failed = 0
	for i, test in enumerate(test_data):
		# Display the index of the test
		print(f"=== Test {i+1} out of {len(test_data)} ===")

		# Perform the function. If an error is raised due to a syntax or any other error, let it be raised
		result = func(*test)
		
		# Check if the result can be raised by checking if it inherits the Exception class
		if type(result) not in Exception.__subclasses__():
			print(PASS_TEXT)
			tests_passed += 1
		else:
			print(FAILED_TEXT)
			# Only raise the result if the parameter says to do so. Parameter defaults as True
			if raise_error: raise result
			# Display result if not raised so that the result may still be understood.
			print(result)
			# Increment the number of tests failed variable
			tests_failed += 1
	
	# Display the number of tests passed and the number of tests failed.
	print(f"{Chromify.Fore.color(GREEN)}{tests_passed} Test(s) passed.")
	# Reset the colour to white at the end so it displays normally.
	print(f"{Chromify.Fore.color(RED)}{tests_failed} Test(s) Failed.{Chromify.Fore.color(WHITE)}")

if __name__=="__main__":
	pass
