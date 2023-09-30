import argparse
import matplotlib.pyplot as plt


def removeUnknown(filePath):
    companies = []

    with open(filePath, "r") as file:
        for line in file:
            if not line.strip().endswith("Not Found"):
                parts = line.strip().split(" - ")
                if len(parts) == 2:
                    company = parts[1]  # company name
                    companies.append(company)

    return companies


def countCompanies(companies):
    companyCount = {}
    for company in companies:
        if company in companyCount:
            companyCount[company] += 1
        else:
            companyCount[company] = 1
    return companyCount


def makeChart(companies, title="MAC Address Vendors"):
    companyCount = countCompanies(companies)

    companies = list(companyCount.keys())
    counts = list(companyCount.values())

    plt.figure(figsize=(10, 10))
    plt.pie(counts, labels=companies, autopct="%1.1f%%")
    plt.title(title)
    plt.axis("equal")
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Input file")
    args = parser.parse_args()

    companies = removeUnknown(args.file)
    makeChart(companies)
