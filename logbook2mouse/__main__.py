import logging
from pathlib import Path
import sys
import argparse

from logbook2mouse.logbook_reader import Logbook2MouseReader
from logbook2mouse.measurement_script import MeasurementScript

def configure_logging(log_level: int, log_to_file: bool = False, log_file_path: str = "logbook2mouse.log"):
    # Create a logger
    logger = logging.getLogger("logbook2mouse")
    logger.setLevel(log_level)

    # Create console handler for logging to stdout
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)  # Log level for console

    # Create a formatter and add it to the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    # Add the console handler to the logger
    logger.addHandler(console_handler)

    # Optionally log to a file
    if log_to_file:
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(log_level)  # Log level for file
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Avoid duplicate logs by ensuring no duplicate handlers are added
    logger.propagate = False

    return logger

def parse_args():
    parser = argparse.ArgumentParser(description="Logbook to Measurement Script Generator")

    # Required arguments
    parser.add_argument("logbook_file", type=Path, help="Path to the logbook Excel file")
    parser.add_argument("protocols_directory", type=Path, help="Path to the directory containing protocol files")
    parser.add_argument("output_script_file", type=Path, help="Path to save the generated measurement script to")

    # Optional arguments
    parser.add_argument("-v", "--verbosity", action="count", default=0,
                        help="Increase output verbosity (e.g., -v for INFO, -vv for DEBUG)")
    parser.add_argument("--log_file", type=str, default=None,
                        help="Path to the optional logging output file")
    parser.add_argument("-V", "--validate", action="store_true", 
                        help="Validate the generated script before execution")

    parser.add_argument(
        "-c",
        "--collate",
        action="store_true",
        help="Collate the measurements by configuration",
    )
    return parser.parse_args()


if __name__ == "__main__":
    # Parse arguments
    args = parse_args()

    # Determine log level based on verbosity
    if args.verbosity >= 2:
        log_level = logging.DEBUG
    elif args.verbosity == 1:
        log_level = logging.INFO
    else:
        log_level = logging.WARNING

    # Configure logging
    logger = configure_logging(log_level=log_level, log_to_file=bool(args.log_file), log_file_path=args.log_file if args.log_file else "logbook2mouse.log")

    # Log the arguments received (useful for debugging)
    logger.info(f"Received arguments: {args}")

    # Resolve paths
    logbook_path = Path(args.logbook_file)
    # check if the logbook file exists
    assert logbook_path.is_file(), f"Logbook file not found: {logbook_path}"

    # check if the protocols directory exists
    protocols_directory = Path(args.protocols_directory)
    assert protocols_directory.is_dir(), f"Protocols directory not found: {protocols_directory}"

    # create output script directory if it does not exist
    output_script_path = Path(args.output_script_file)
    output_script_path.parent.mkdir(parents=True, exist_ok=True)
    assert output_script_path.parent.is_dir(), f"Output directory not found: {output_script_path.parent}"
    # check writing permissions
    try: 
        output_script_path.touch()
    except Exception as e:
        logger.error(f"Cannot write to output script file location with error: {e}")
        sys.exit(1)

    # Log paths for debugging
    logger.info(f"Logbook file path: {logbook_path}")
    logger.info(f"Protocols directory path: {protocols_directory}")
    logger.info(f"Output script file path: {output_script_path}")

    # Example usage
    try:
        reader = Logbook2MouseReader(logbook_path)
        script = MeasurementScript(
            entries=reader.entries,
            protocols_directory=protocols_directory,
            output_script_path=output_script_path,
            collate=args.collate,
        )

        # Validate the script if the -V flag is provided
        if args.validate:
            logger.info("Validating the measurement script...")
            try:
                script.validate()
                logger.info("Validation passed successfully.")
            except Exception as e:
                logger.error(f"Validation failed with error: {e}")
                sys.exit(1)

        # Generate the script
        script.save_script(Path(output_script_path))

        logger.info(f"Measurement script saved successfully to: {output_script_path}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise e
        # sys.exit(1)
