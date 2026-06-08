from app.chain.steps import PromptBuilder, PromptBuilderInput, PromptBuilderOutput, ResponseParser, LLMRunnerOutput, ResponseParserOutput

def test_prompt_builder_includes_question_and_stats():
    builder = PromptBuilder()
    input_data = PromptBuilderInput(question="What is the average age?", stats_summary="age: mean=30")

    output = builder.invoke(input_data)
    assert isinstance(output, PromptBuilderOutput)
    assert "What is the average age?" in output.prompt
    assert "age: mean=30" in output.prompt


def test_response_parser_strips_whitespace():
    parser = ResponseParser()
    input_data = LLMRunnerOutput(raw_text= "  hello there  ")
    output = parser.invoke(input_data)

    assert isinstance(output, ResponseParserOutput)
    assert output.answer == "hello there"
