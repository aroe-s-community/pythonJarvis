import csv

class CSV:
    # Contents should be a list of dictionaries
    @staticmethod
    def appendDict(filename, contents):
        # If contents is empty just exit and don't write anything
        if not contents:
            return

        # Get list of fields
        fields = []
        for key in contents[0].keys():
            fields.append(key)

        print(fields)

        # Open csv file
        with open(filename, mode='a') as fp:
            writer = csv.DictWriter(fp, fieldnames=fields, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            writer.writeheader()

            # Write each article to csv
            for c in contents:
                writer.writerow(c)

    @staticmethod
    def append(filename, contents):
        # Open csv file
        with open(filename, mode='a') as fp:
            headline_writer = csv.writer(fp, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            # Write each article to csv
            for c in contents:
                headline_writer.writerow(c)

    # Clear a csv file
    @staticmethod
    def clear(filename):
        with open(filename, mode='w') as fp:
            fp.close()
