
import json
import io
import zipfile

from epyk.core.html import Html

# The list of CSS classes
# from epyk.core.css.styles import CssGrpClsFile
# from epyk.core.css.styles import GrpClsButton


class DownloadMemoryZip(Html.Html):
  """

  TODO Find a way to send the in memory file form a report: data: %(archive)s,
  """
  alias, cssCls, __reqCss = 'anchorFMemory', ['btn', 'btn-success'], ['font-awesome', 'bootstrap']
  name, category = 'Memory Files', 'System'
  builder_name = False
  # CSS Classes
  #_grpCls = CssGrpClsButton.CssClassButton

  def __init__(self, report, vals, fileName, cssCls, cssAttr, profile):
    super(DownloadMemoryZip, self).__init__(report, vals,  cssCls, cssAttr, profile=profile)
    self.fileName = fileName
    self.memory_file = io.BytesIO()
    self.zf = zipfile.ZipFile(self.memory_file, mode='w', compression=zipfile.ZIP_DEFLATED)

  def add(self, data, filename):
    """ Add the content of string to a file in the in-memory package

    :param data: The data
    :param filename: The filename

    :return:
    """
    self.zf.writestr(filename, data)

  def namelist(self):
    """ Return the list of files in the in-memory zip archive

    :return:
    """
    return self.zf.namelist()

  def __str__(self):
    self.click('''
        $.ajax({url: %(url)s, type: "POST", contentType: attr("enctype", "multipart/form-data"), data: '%(archive)s', success: success})
        ''' % {'url': "''", 'archive': '' #self.zf
               })
    return '<button %s>%s</button>' % (self.get_attrs(pyClassNames=self.style.get_classes()), self.val)


class DropFile(Html.Html):
  requirements = ('font-awesome', 'bootstrap')
  name, inputType = 'Drop File Area', "file"
  #_grpCls = CssGrpClsFile.CssStylesDrop

  def __init__(self, report, vals, tooltip, report_name, file_type, profile):
    super(DropFile, self).__init__(report, vals, profile=profile)
    self.tooltip(tooltip, location='bottom')
    self.report_name, self.dataType = report_name if report_name is not None else self._report.run.report_name, file_type
    for action in ["dragover", "dragleave", "dragenter"]:
      self.jsFrg(action, "event.originalEvent.preventDefault(); event.originalEvent.stopPropagation(); event.originalEvent.dataTransfer.dropEffect = 'copy';")
    self.css({"display": "inline-block", "width": '100%'})

  @property
  def jsQueryData(self): return {}

  def drop(self, url=None, jsData=None, jsFncs=None, httpCodes=None, isPyData=True, refresh=True, extensions=None):
    data = []
    if url is None:
      url = "%s/upload/OUTPUTS/%s" % (self._report._urlsApp['epyk-transfer'], self.report_name)
    if jsFncs is None:
      jsFncs = [self._report.jsReloadPage()]
    elif not isinstance(jsFncs, list):
      jsFncs = [jsFncs]

    if jsData is not None:
      for rec in jsData:
        if isinstance(rec, tuple):
          if isPyData:
            data.append("data.append('%s', %s)" % (rec[0], json.dumps(rec[1])))
          else:
            data.append("data.append('%s', %s)" % (rec[0], rec[1]))
        else:
          data.append("data.append('%s', %s)" % (rec.htmlCode, rec.val))
    super(DropFile, self).drop('''
      event.originalEvent.preventDefault(); event.originalEvent.stopPropagation();
      var files = event.originalEvent.dataTransfer.files; var data = new FormData();
      $.each(event.originalEvent.dataTransfer.files, function(i, file) { 
        var fileExt = '.' + file.name.split('.').pop();
        if(%(extensions)s == null) {data.append(file.name, file)} else {
          if(%(extensions)s.indexOf(fileExt) >= 0) { data.append(file.name, file)}}});
      %(jsData)s; %(ajax)s''' % {"jsData": ";".join(data), "extensions": json.dumps(extensions),
                                 "ajax": self._report.jsAjax(url, success=";".join(jsFncs) if refresh else '' ) })
    return self

  def __str__(self):
    return '''
      <div %(strAttr)s><b><i class="fas fa-cloud-upload-alt" style="font-size:20px"></i>&nbsp;&nbsp;%(vals)s</b></div>
      <input id="%(htmlCode)s_report" style="display:none;" value="%(envs)s"/>
      ''' % {'htmlCode': self.htmlCode, 'strAttr': self.get_attrs(pyClassNames=self.style.get_classes()), 'vals': self.vals, 'envs': self.report_name}


class DropConfiguration(Html.Html):
  requirements = ('font-awesome', 'bootstrap')
  #_grpCls = CssGrpClsFile.CssStylesDrop
  name, inputType = 'Drop Configuration Area', "file"

  def __init__(self, report, vals, htmlCode, url, tablename):
    super(DropConfiguration, self).__init__(report, vals, htmlCode=htmlCode)
    self.tooltip('Drop your files here', location='bottom')
    self.code = htmlCode
    for action in ["dragover", "dragleave", "dragenter"]:
      self.jsFrg(action, "event.originalEvent.preventDefault(); event.originalEvent.stopPropagation(); event.originalEvent.dataTransfer.dropEffect = 'copy';")
    self.css({"display": "inline-block", "width": '100%'})
    super(DropConfiguration, self).drop('''
          event.originalEvent.preventDefault(); event.originalEvent.stopPropagation();
          var files = event.originalEvent.dataTransfer.files; var data = new FormData();
          $.each(event.originalEvent.dataTransfer.files, function(i, file) { 
            var fileExt = '.' + file.name.split('.').pop() ; data.append(file.name, file) ;}); %(ajax)s; ''' % {
                                    "ajax": self._report.jsAjax('%s/%s/%s/%s/%s' % (url, self._report.run.report_name, self._report.run.script_name, self.code, tablename)
                                                                                 ,success=self._report.jsReloadPage())})


  @property
  def jsQueryData(self): return {}

  def __str__(self):
    return '''
      <div %(strAttr)s><b><i class="fas fa-cloud-upload-alt" style="font-size:20px"></i>&nbsp;&nbsp;%(vals)s</b></div>
      <input id="%(htmlCode)s_report" style="display:none;" value="%(envs)s"/>
      ''' % {'htmlCode': self.htmlCode, 'strAttr': self.get_attrs(pyClassNames=self.style.get_classes()), 'vals': self.vals, 'envs': self._report.run.report_name}
