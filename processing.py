import os
import datetime
import pandas as pd

from typing import Generator


def read_data(source_dir: str) -> Generator:
    # reading all file with .dat extesion from the source folder

    for filename in os.listdir(source_dir):
        if filename.endswith(".dat"):
            file_path = os.path.join(source_dir, filename)
            try:
                with open(file_path, "r") as fp:
                    while line := fp.readline():
                        yield line
            except FileNotFoundError:
                print(f"ERROR: File `{filename=}` not found in `{source_dir=}`")
            except Exception as e:
                print(f"ERROR: While processig file `{filename=}`: {e}")


def pre_process(source_dir: str) -> pd.DataFrame:
    # make a call to read_data generator and clean the lines one by one to
    # save it somewhere in list

    data_list = []
    for line in read_data(source_dir):
        line = [column.strip() for column in line.strip().split("\t")]
        data_list.append(line)

    if data_list:
        return pd.DataFrame(data_list[1:], columns=data_list[0])

    # return empty dataframe if no .dat file exists in SOURCE_DIR
    print(f"WARNING: No .dat file found in the specified {source_dir=} folder.")
    return pd.DataFrame()


def average_salary(dataframe: pd.DataFrame) -> pd.Series | float | int:
    return dataframe["gross_salary"].astype(float).mean()


def nth_largest_salary(top: int, nth: int, dataframe: pd.DataFrame) -> float:
    # this function holds `top` specified records and returns `nth` records
    # from the provided dataframe
    return (
        dataframe.nlargest(
            top,
            "gross_salary",
            keep="all",
        ).iloc[nth]["gross_salary"]
        if not dataframe.empty
        else 0
    )


def write_result_to_csv(dataframe: pd.DataFrame, target_dir: str) -> None:
    # wrtting dataframe content to the specified location

    try:
        filepath = f"{target_dir}/{datetime.datetime.now(datetime.UTC).timestamp()}.csv"
        dataframe.to_csv(filepath, sep=",", index=False)
        print(f"INFO: Saved at file: {filepath=}")
    except Exception as e:
        print(f"ERROR: While saving dataframe as CSV. \n {e}")


def processing(source_dir: str, target_dir: str) -> None:
    # process the .dat files

    try:
        dataframe = pre_process(source_dir)
        if not dataframe.empty:
            if (
                "basic_salary" not in dataframe.columns
                or "allowances" not in dataframe.columns
            ):
                print(
                    f"INFO: Desired columns (`basic_salary`, `allowances`) does not exists in {dataframe.columns=}."
                )
                return

            # string to numeric conversion of basic_salary and allowances
            dataframe["basic_salary"] = pd.to_numeric(
                dataframe["basic_salary"], errors="coerce"
            )
            dataframe["allowances"] = pd.to_numeric(
                dataframe["allowances"], errors="coerce"
            )

            # calculate gross_salary = basic_salary + allowances
            dataframe["gross_salary"] = (
                dataframe["basic_salary"] + dataframe["allowances"]
            )

            resultant_dataframe = pd.DataFrame(
                {
                    "id": [
                        f"Second Highest Salary={nth_largest_salary(5, 2, dataframe)}"
                    ],
                    "first_name": [f"Average Salary={average_salary(dataframe)}"],
                    "last_name": [""],
                    "email": [""],
                    "job_title": [""],
                    "basic_salary": [""],
                    "allowances": [""],
                    "gross_salary": [""],
                },
                columns=dataframe.columns,
            )

            # to rmove duplicates from existing dataframe and it is inplace change
            dataframe.drop_duplicates(inplace=True)

            # concatinated desired results to the end of dataframe
            dataframe = pd.concat([dataframe, resultant_dataframe])

            # save dataframe to the CSV file
            write_result_to_csv(dataframe, target_dir)
        else:
            print("INFO: Nothing to process.")
    except Exception as e:
        print(f"ERROR: While processing data: {e}")


if __name__ == "__main__":
    CURRENT_PATH = os.path.abspath(os.path.curdir)
    SOURCE_DIR = f"{CURRENT_PATH}/source"
    TARGET_DIR = f"{CURRENT_PATH}/output"
    processing(SOURCE_DIR, TARGET_DIR)
