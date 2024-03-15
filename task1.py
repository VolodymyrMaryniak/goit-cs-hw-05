import asyncio
import logging
from aiopath import AsyncPath
from aioshutil import copyfile
from typing import AsyncGenerator
from argparse import ArgumentParser, Namespace


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def parse_args() -> Namespace:
    parser = ArgumentParser("Files sorter")
    parser.add_argument(
        "-s", "--source", help="Path to the source directory", required=True
    )
    parser.add_argument(
        "-o", "--output", help="Path to the destination directory", required=True
    )

    args = parser.parse_args()
    return args


async def main():
    args = parse_args()

    source = AsyncPath(args.source)
    output = AsyncPath(args.output)

    if not await source.exists():
        logging.error(f"Source directory {source} does not exist")
        return

    if not await output.exists():
        try:
            await output.mkdir()
        except OSError as e:
            logging.error(f"Error while creating directory {output}: {e}")
            return

    logging.info("Started copying files.")

    async for file in read_folder(source):
        await copy_file(file, output)

    logging.info("Finished copying files.")


async def read_folder(folder: AsyncPath) -> AsyncGenerator[AsyncPath, None]:
    """Recursively iterates files in the folder and its subfolders."""
    async for path in folder.iterdir():
        if await path.is_file():
            yield path
        else:
            async for file in read_folder(path):
                yield file


async def copy_file(file: AsyncPath, destionation_dir: AsyncPath):
    logging.debug(f"Copying {file.name} to {destionation_dir}")

    file_extension = file.suffix
    sub_dir = file_extension[1:] if file_extension else "other"
    ext_dir = destionation_dir / sub_dir

    if not await ext_dir.exists():
        await ext_dir.mkdir()

    destination_file_path = ext_dir / file.name
    try:
        await copyfile(file, destination_file_path)
    except OSError as e:
        logging.error(f"Error while copying {file} to {destination_file_path}: {e}")


if __name__ == "__main__":
    asyncio.run(main())
