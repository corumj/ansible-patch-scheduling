# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
  lookup: patch_day
  author: Jerry Corum <jcorum@redhat.com>
  version_added: "0.1"
  short_description: return desired patch day
  description:
      - This lookup returns a patch day based on the second tuesday of the month plus an offset.
  options:
    _terms:
      description: offset example 18 will provide the date of the second tuesday plus 18 days
      required: True
  notes:
    - only read in variable context
"""
from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display

display = Display()


class LookupModule(LookupBase):

  def run(self, terms, variables=None, **kwargs):
    # lookups in general are expected to both take a list as input and output a list
    # this is done so they work with the looping construct 'with_'.
    ret = []
    for term in terms:
      display.debug("Offset: %s" % term)
      # Don't use print or your own logging, the display class
      # takes care of it in a unified way.
      display.vvvv(u"Second tuesday lookup using %s as offset days" % term)
      try:
        if term:
          import calendar
          from datetime import datetime
          from datetime import timedelta

          # Use todays year and month as a base for the calculation
          year = int(datetime.today().strftime("%Y"))
          month = int(datetime.today().strftime("%m"))

          c = calendar.Calendar(firstweekday=calendar.SUNDAY)

          monthcal = c.monthdatescalendar(year,month)

          # Get the second tuesday of the current month
          second_tuesday = [day for week in monthcal for day in week if \
                          day.weekday() == calendar.TUESDAY and \
                          day.month == month][1]

          # Calculate the desired patch day based of the current month's second tuesday and the offset
          patch_day = second_tuesday + timedelta(days=int(term)) 

          ret.append(patch_day)
        else:
          # Always use ansible error classes to throw 'final' exceptions,
          # so the Ansible engine will know how to deal with them.
          # The Parser error indicates invalid options passed
          raise AnsibleParserError()
      except AnsibleParserError:
        raise AnsibleError("could not calculate date with offset: %s" % term)

    return ret