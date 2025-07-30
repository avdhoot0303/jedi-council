import logging

def test_logging_structure(caplog):
    logger = logging.getLogger("jedi_council.core")
    with caplog.at_level(logging.INFO):
        logger.info("Testing log output")
    assert any("Testing log output" in message for message in caplog.messages)
