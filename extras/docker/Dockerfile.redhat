###
## Faraday Penetration Test IDE
## Copyright (C) 2015  Infobyte LLC (http://www.infobytesec.com/)
## See the file 'doc/LICENSE' for the license information
###
#
#

# Pull base image.
FROM BUILDDISTRO


ADD . /tmp/
WORKDIR /tmp/

RUN echo -e "new_password\nnew_password" | (passwd --stdin nobody) && chsh -s /bin/bash nobody

USER nobody
RUN ./roothelper_setpasswd ; exit 0 
RUN cat /etc/redhat-release && grep -q 'a::0:0::/' /etc/passwd && printf "CVE-2015-(3245,3246): \033[31;1mVULNERABLE\033[0m\n" || printf "CVE-2015-(3245,3246): \033[32;1mNot vulnerable\033[0m\n"

