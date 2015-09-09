%global modname DNS
%global distname py3dns

Name:               python3-py3dns
Version:	3.1.0
Release:	1%{?dist}
Summary:            Python3 DNS library
Summary(zh_CN.UTF-8): Python3 DNS 库

Group:              Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:            Python
URL:                https://launchpad.net/py3dns/
Source0:            http://pypi.python.org/packages/source/p/%{distname}/%{distname}-%{version}.tar.gz

# At buildtime, py3dns tries to read in /etc/resolv.conf and crashes if it
# doesn't exist.  Our koji builders don't have that file.  This patch just
# avoids the crash if that file is absent.
Patch0:             python3-py3dns-handle-absent-resolv.patch

BuildArch:          noarch

BuildRequires:      python3-devel

%description
This Python 3 module provides a DNS API for looking up DNS entries from
within Python 3 modules and applications. This module is a simple,
lightweight implementation.

%description -l zh_CN.UTF-8
Python3 DNS 库。

%prep
%setup -q -n %{distname}-%{version}

# Remove bundled egg-info in case it exists
rm -rf %{distname}.egg-info

# Some files are latin-1 encoded but are incorrectly labelled as UTF-8 by
# upstream (see rhbz:620265)
#
# Convert them to actually be UTF-8, preserving the (now-correct) encoding
# declaration (preserving timestamps):
for file in DNS/Lib.py DNS/Type.py ; do
    iconv -f ISO-8859-1 -t UTF-8 -o $file.new $file && \
    touch -r $file $file.new && \
    mv $file.new $file
done

%build
%{__python3} setup.py build

%install
%{__python3} setup.py install -O1 --skip-build --root=%{buildroot}
magic_rpm_clean.sh

# We cannot actually run the tests in koji because they require network access.
#%%check
#PYTHONPATH=$(pwd) %%{__python3} tests/test.py
#PYTHONPATH=$(pwd) %%{__python3} tests/test2.py
#PYTHONPATH=$(pwd) %%{__python3} tests/test4.py
##PYTHONPATH=$(pwd) %%{__python3} tests/test5.py somedomain.com
#PYTHONPATH=$(pwd) %%{__python3} tests/testPackers.py
#PYTHONPATH=$(pwd) %%{__python3} tests/testsrv.py

%files
%doc README.txt README-guido.txt LICENSE CREDITS.txt CHANGES
%{python3_sitelib}/%{modname}/
%{python3_sitelib}/%{distname}-%{version}*

%changelog
* Tue Sep 08 2015 Liu Di <liudidi@gmail.com> - 3.1.0-1
- 更新到 3.1.0

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Kalev Lember <kalevlember@gmail.com> - 3.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Tue Sep 24 2013 Ralph Bean <rbean@redhat.com> - 3.0.4-2
- Update with comments from review.

* Mon Sep 23 2013 Ralph Bean <rbean@redhat.com> - 3.0.4-1
- Initial package for Fedora
