class WeblogPingerPlugin(EventPlugin):
    EventType = EventType.AFTERPUBLISH
    Name = "Weblog Pinger"
    
    def handle(self, parent, evt):
        parent.notifier.info("Pinging Weblogs...")
        from xmlrpclib import Server
        server = Server("http://rpc.weblogs.com/RPC2")
        blog = parent.account.Blogs[parent.account.SelectedBlog]
        res = server.weblogUpdates.ping (str(blog.Name), str(blog.Url))
        if res['flerror']:
            parent.notifier.error("Failed!")
            print "got this error while pinging: "+res['message']
        else:
            parent.notifier.info("Done!")
            