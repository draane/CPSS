from xml.dom.minidom import parse
import os

NODE_ID_REMOVE_LIST = ["toomanyconfigs"]


def clean_report(filename, new_file):
    print(filename, new_file)
    report = parse(filename)
    results = report.documentElement
    for error in results.childNodes:
        if error.nodeName == "#text":
            continue

        if error.nodeName == "error":
            if error.hasAttribute("file"):
                error.attributes['file'].value = error.attributes['file'].value.replace("temp/", "")

                if "test" in error.attributes['file'].value:
                    error.unlink()
                    continue

            if str(error.getAttribute('id')) in NODE_ID_REMOVE_LIST:
                error.unlink()
        else:
            error.unlink()

    file_handle = open(new_file, "w")
    report.writexml(file_handle)
    file_handle.close()


def main():
    report_list = os.listdir('reports/')
    for report in report_list:
        report_path = "./reports/" + report
        cleaned_report_path = "clean_reports/" + report
        try:
            clean_report(report_path, cleaned_report_path)
        except:
            pass


if __name__ == '__main__':
    main()
