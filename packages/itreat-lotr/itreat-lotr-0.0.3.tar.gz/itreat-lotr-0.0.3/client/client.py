import api, sys, json

def show_data(type, filter=None, limit=None):
    print(api.get_all_data(type, filter, limit))

def is_filter_param(argv):
    if len(argv) > 2:
        filter = sys.argv[2]
        return filter

def is_filter_activated(argv):
    if len(argv) > 3:
        limit = sys.argv[3]
        return limit

def main():
    try:
        show_data(sys.argv[1], is_filter_param(sys.argv), is_filter_activated(sys.argv))
    except IndexError:
        print("Please refer to the Documentation for parameters.")
    except json.decoder.JSONDecodeError:
        print("There didn't seem to be a match. Double check spelling and try again.")