import wx
import shelve

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.CAPTION | wx.CLIP_CHILDREN | wx.CLOSE_BOX | wx.RESIZE_BORDER | wx.SYSTEM_MENU
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((170, 446))
        self.SetTitle("$MSG Tools")

        self.panel_1 = wx.Panel(self, wx.ID_ANY)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        self.text_ctrl_1 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "*.d")
        sizer_1.Add(self.text_ctrl_1, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        self.button_1 = wx.Button(self.panel_1, wx.ID_ANY, "Get Headers")
        sizer_1.Add(self.button_1, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        self.check_list_box_1 = wx.CheckListBox(self.panel_1, wx.ID_ANY,
                                                choices=["choice 1"])
        self.check_list_box_1.SetMinSize((100, 300))
        sizer_1.Add(self.check_list_box_1, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        self.button_2 = wx.Button(self.panel_1, wx.ID_ANY, "Export Data")
        sizer_1.Add(self.button_2, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        self.panel_1.SetSizer(sizer_1)

        self.Layout()

        self.Bind(wx.EVT_BUTTON, self.get_headers, self.button_1)
        self.Bind(wx.EVT_BUTTON, self.export_data, self.button_2)
        # end wxGlade

    def get_headers(self, event):  # wxGlade: MyFrame.<event_handler>
        data = []

        extension = self.text_ctrl_1.GetValue()

        path = MyFileDialog(None, wildcard=extension)
        files = path.EventHandler.Paths

        for file_no in range(0, len(files)):

            try:
                f = open(files[file_no], "r")
                # print(file_list[file_no]) # Print file name
                for line in f:
                    data.append(line)
            except:
                print("error in file {0}".format(files[file_no]))

        headers = dict.fromkeys([line.rsplit(",")[0] for line in data
                                 if len(line.rsplit(',')) > 1])
        headers = list(headers)

        self.check_list_box_1.SetItems(headers)

        data_out = shelve.open('data')
        data_out['headers'] = headers
        data_out['files'] = files
        data_out.close()

        event.Skip()

    def export_data(self, event):  # wxGlade: MyFrame.<event_handler>
        headers = self.check_list_box_1.GetCheckedStrings()

        # self.showDialog(None)
        # for header in headers:
        #     print(header)
        path = MyNewFileDialog(None)
        output_file = path.EventHandler.Path
        print(output_file)

        with shelve.open('data') as db:
            headers_stored = db['headers']
            files = db['files']

        print(files)

        with open(output_file, 'w') as out:
            for file in files:
                with open(file, 'r') as data_file:
                    for line in data_file:
                        for header in headers:
                            if line.startswith(header):
                                # print(line)
                                out.write(line)
        print(headers)
        event.Skip()

    def SelectFrame(self, headers):
        window3 = SelectMessages(None, wx.ID_ANY, "")

    def showDialog(self, headers): # wxGlade: MyMainFrame.<event_handler>
        # SelectMessages(self).Show()
        # newframe = SelectMessages()
        # newframe.setChoices(headers)
        # newframe.Show()
        headers = self.check_list_box_1.GetCheckedStrings()
        newframe = SelectMessages(self)
        newframe.check_list_box_2.SetItems(headers)
        newframe.Show()

# end of class MyFrame


class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

# end of class MyApp


class MyFileDialog(wx.FileDialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFileDialog.__init__
        kwds["style"] = kwds.get("style", 0) | wx.FD_OPEN | \
                        wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE
        wx.FileDialog.__init__(self, *args, **kwds)
        self.SetTitle("Select files")

        self.ShowModal()
# end of class MyFileDialog


class SelectMessages(wx.Frame):
    def __init__(self, *args, **kwds):
    # def __init__(self, data, *args, **kwds):
        # begin wxGlade: SelectMessages.__init__
        kwds["style"] = kwds.get("style", 0) | wx.CAPTION | wx.CLIP_CHILDREN | \
                        wx.CLOSE_BOX | wx.RESIZE_BORDER | wx.SYSTEM_MENU
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((136, 449))
        self.SetTitle("frame_1")

        self.panel_1 = wx.Panel(self, wx.ID_ANY)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        self.check_list_box_2 = wx.CheckListBox(self.panel_1, wx.ID_ANY)
        self.check_list_box_2.SetMinSize((100, 400))
        sizer_1.Add(self.check_list_box_2, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        self.panel_1.SetSizer(sizer_1)

        self.Layout()

        self.Bind(wx.EVT_CLOSE, self.write_file, self)

        # end wxGlade

    def write_file(self, event):  # wxGlade: SelectMessages.<event_handler>
        print("Not yet close window")
        event.Skip()

# end of class SelectMessages


class MyNewFileDialog(wx.FileDialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.FD_SAVE
        kwds['defaultFile'] = 'data.csv'
        wx.FileDialog.__init__(self, *args, **kwds)
        self.SetTitle("Enter filename")

        self.ShowModal()
# end of class MyFileDialog


if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
