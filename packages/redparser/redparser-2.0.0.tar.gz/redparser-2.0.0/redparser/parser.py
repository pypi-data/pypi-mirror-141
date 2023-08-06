import mmap
import re
import ipaddress

from .highlight import highlighter_ipv4, highlighter_ipv6, highlight_both

class Parser():

    def __init__(self, file_obj, arguments):

        self.arguments = arguments

        # will this creat a copy, need to make sure it doesn't
        self.file_obj = file_obj
        self.num_lines = -1

        if self.arguments.mmap:
            self.engine = self.mmap_first
        else:
            self.engine = self.memory_first

        self.output = print

        # simple returning first or last lines
        self.simple = 1

        # first number of lines given
        if self.arguments.first:
            self.num_lines = self.arguments.first

        # last number of lines given
        if self.arguments.last:
            self.num_lines = self.arguments.last
            if self.arguments.mmap:
                self.engine = self.mmap_last
            else:
                self.engine = self.memory_last

        # parser is no longer simple, more parsing required
        if self.arguments.ipv6 or self.arguments.ipv4 or self.arguments.timestamps:
            self.simple = 0

            # set highlight
            if self.arguments.ipv4: self.output = highlighter_ipv4
            if self.arguments.ipv6: self.output = highlighter_ipv6
            if self.arguments.ipv6 and self.arguments.ipv4: self.output = highlight_both

    def followup(self, line):
        # search for timestamps
        if self.arguments.timestamps:
            timestamp_found = self.timestamps(line)
            if timestamp_found:
                # check to search for ip addresses
                if self.arguments.ipv4:
                    ipv4_found = self.ipv4(line)
                    if ipv4_found == 0 and self.arguments.ipv6:
                        return self.ipv6(line)
                    return ipv4_found
                # check but only for ipv6 addressses
                if self.arguments.ipv6:
                    return self.ipv6(line)
            # no timestamp found
            return timestamp_found

        # don't need to search for timestamps, only ip addresses
        if self.arguments.ipv4:
            ipv4_found = self.ipv4(line)
            if ipv4_found == 0 and self.arguments.ipv6:
                return self.ipv6(line)
            return ipv4_found

        if self.arguments.ipv6:
            return self.ipv6(line)

        # no follow up arguments
        return 0

    def mmap_first(self):
        try:
            with mmap.mmap(self.file_obj.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_obj:
                file_length = len(mmap_obj)-1
                startpointer = 0
                endpointer = 0
                found_items=[]
                while self.num_lines != 0 and endpointer < file_length:
                    endpointer = mmap_obj.find(b'\n', startpointer, file_length) + 1
                    # end of file
                    if endpointer == 0:
                        endpointer = file_length+1

                    if self.simple:
                        self.num_lines -= 1
                    else:
                        # shift by one to be like first
                        success = self.followup(mmap_obj[startpointer:endpointer])
                        if success:
                            found_items.append([startpointer, endpointer])
                            self.num_lines -= 1


                    startpointer = endpointer

                if self.simple:
                    return mmap_obj[:endpointer].decode('utf-8')
                else:
                    result = ""
                    for item in found_items:
                        result += mmap_obj[item[0]:item[1]].decode('utf-8')
                    return result.rstrip('\n')

        except Exception as e:
            print(e)

    def mmap_last(self):
        try:
            with mmap.mmap(self.file_obj.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_obj:
                file_length = len(mmap_obj) - 1
                startpointer = file_length
                endpointer = file_length+1 # to get last byte of end of file
                #have to track pointers to print logs in reverse order
                found_items = []
                # is it safe for startpointer > 0
                while self.num_lines != 0 and startpointer > 0:
                    startpointer = mmap_obj.rfind(b'\n', 0, endpointer)

                    if self.simple:
                        self.num_lines -= 1
                    else:
                        # shift by one to be like first
                        success = self.followup(mmap_obj[startpointer + 1:endpointer + 1])
                        if success:
                            found_items.insert(0, [startpointer + 1, endpointer + 1])
                            self.num_lines -= 1

                    endpointer = startpointer

                if self.simple:
                    return mmap_obj[startpointer+1:].decode('utf-8')
                else:
                    result = ""
                    for item in found_items:
                        result += mmap_obj[item[0]:item[1]].decode('utf-8')

                    return result.rstrip('\n')

        except Exception as e:
            print(e)

    def memory_first(self):
        try:
            file_length = len(self.file_obj) - 1
            startpointer = 0
            endpointer = 0
            found_items = []
            while self.num_lines != 0 and endpointer < file_length:
                endpointer = self.file_obj.find(b'\n', startpointer, file_length) + 1

                # end of file
                if endpointer == 0:
                    endpointer = file_length + 1

                if self.simple:
                    self.num_lines -= 1
                else:
                    # shift by one to be like first
                    success = self.followup(self.file_obj[startpointer:endpointer])
                    if success:
                        found_items.append([startpointer, endpointer])
                        self.num_lines -= 1

                startpointer = endpointer

            if self.simple:
                return self.file_obj[:endpointer].decode('utf-8')
            else:
                result = ""
                for item in found_items:
                    result += self.file_obj[item[0]:item[1]].decode('utf-8')
                return result.rstrip('\n')

        except Exception as e:
            print(e)

    def memory_last(self):
        try:
            file_length = len(self.file_obj) - 1
            startpointer = file_length
            endpointer = file_length
            # have to track pointers to print logs in reverse order
            found_items = []
            # is it safe for startpointer > 0
            while self.num_lines != 0 and startpointer > 0:
                startpointer = self.file_obj.rfind(b'\n', 0, endpointer)

                if self.simple:
                    self.num_lines -= 1
                else:
                    # shift by one to be like first
                    success = self.followup(self.file_obj[startpointer + 1:endpointer + 1])
                    if success:
                        found_items.insert(0, [startpointer + 1, endpointer + 1])
                        self.num_lines -= 1

                endpointer = startpointer

            if self.simple:
                return self.file_obj[startpointer + 1:].decode('utf-8')
            else:
                result = ""
                for item in found_items:
                    result += self.file_obj[item[0]:item[1]].decode('utf-8')
                return result.rstrip('\n')

        except Exception as e:
            print(e)

    def timestamps(self, line):

        if line:
            pattern = re.compile(rb'(?:[01]\d|2[0123]):(?:[012345]\d):(?:[012345]\d)')

            if len(pattern.findall(line)):
                return line

        # timestamp not found
        return 0

    def ipv4(self, line):

        if line:

            pattern = re.compile(rb'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
            ips = pattern.findall(line)

            if len(ips):
                for ip in ips:
                    try:
                        ipaddress.IPv4Address(ip.decode('utf-8'))
                        # found ipv4
                        return line
                    except Exception as e:
                        pass

        # ipv4 not found
        return 0

    def ipv6(self, line):

        if line:
            pattern = rb'^.*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?'

            if re.match(pattern, line):
                # found ipv6
                return line

        # ipv6 not found
        return 0

    def run(self):
        self.output(self.engine())
