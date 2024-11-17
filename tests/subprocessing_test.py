import subprocessmagic

_COMMAND: str = "&&".join(
	[
		"echo 'Hello world!'",
		"sleep 0.42",
		"echo 'This is some developer in the midnight.'",
		"sleep 0.42",
		">&2 echo 'Oh no, a wild bug occurred (O_O)'",
		"exit 24",
	]
)
_EXPECTED_STDOUT: str = "Hello world!\nThis is some developer in the midnight.\n"
_EXPECTED_STDERR: str = "Oh no, a wild bug occurred (O_O)\n"
_EXPECTED_RETURN_CODE: int = 24


class _Result:
	def __init__(self, output: str, return_code: int, error: str) -> None:
		self.output = output
		self.return_code = return_code
		self.error = error


def _assert_result(expected: _Result, actual: _Result):
	assert expected.output == actual.output, "Output is not as expected."
	assert expected.return_code == actual.return_code, "Return Code is not as expected."
	assert expected.error == actual.error, "Error is not as expected."


def test_process():
	import logging

	command = ["bash", "-c", _COMMAND]

	output: str = ""
	error: str = ""

	def _logger(log_level: subprocessmagic.LOG_LEVEL_TYPE, msg: subprocessmagic.OUTPUT_TYPE):
		nonlocal output
		nonlocal error
		if log_level == logging.INFO:
			output += msg
		elif log_level == logging.ERROR:
			error += msg
		else:
			assert False, f"Unexpected logging level: {log_level}"

	return_code = subprocessmagic.process(command=command, logger=_logger)
	_assert_result(
		expected=_Result(output=_EXPECTED_STDOUT, return_code=_EXPECTED_RETURN_CODE, error=_EXPECTED_STDERR),
		actual=_Result(output=output, return_code=return_code, error=error),
	)


def test_run():
	command = ["bash", "-c", _COMMAND]
	output, return_code, error = subprocessmagic.run(command=command)
	_assert_result(
		expected=_Result(output=_EXPECTED_STDOUT, return_code=_EXPECTED_RETURN_CODE, error=_EXPECTED_STDERR),
		actual=_Result(output=output, return_code=return_code, error=error),
	)


def test_shell():
	command = _COMMAND
	output, return_code, error = subprocessmagic.shell(command=command)
	_assert_result(
		expected=_Result(output=_EXPECTED_STDOUT, return_code=_EXPECTED_RETURN_CODE, error=_EXPECTED_STDERR),
		actual=_Result(output=output, return_code=return_code, error=error),
	)
