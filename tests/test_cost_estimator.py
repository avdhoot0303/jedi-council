def test_cost_calculation():
    from jedi_council.utils.utils import estimate_cost

    cost = estimate_cost("gpt-4o", input_tokens=100, output_tokens=400)
    assert isinstance(cost, float)
    assert cost > 0
