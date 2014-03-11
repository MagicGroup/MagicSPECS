# Reflects the values hard-coded in various Makefile.am's in the source tree.
%define dictdir %{_datadir}/cracklib
%define dictpath %{dictdir}/pw_dict

Summary: A password-checking library
Name: cracklib
Version: 2.8.18
Release: 4%{?dist}
Group: System Environment/Libraries
Source0: http://prdownloads.sourceforge.net/cracklib/cracklib-%{version}.tar.gz

# Retrieved at 20091201191719Z.
Source1: http://iweb.dl.sourceforge.net/project/cracklib/cracklib-words/2008-05-07/cracklib-words-20080507.gz

# For man pages.
Source2: http://ftp.us.debian.org/debian/pool/main/c/cracklib2/cracklib2_2.8.18-1.debian.tar.gz

# From attachment to https://bugzilla.redhat.com/show_bug.cgi?id=627449
Source3: cracklib.default.zh_CN.po

Source10: http://ftp.cerias.purdue.edu/pub/dict/wordlists/computer/Domains.gz
Source11: http://ftp.cerias.purdue.edu/pub/dict/wordlists/computer/Dosref.gz
Source12: http://ftp.cerias.purdue.edu/pub/dict/wordlists/computer/Ftpsites.gz
Source13: http://ftp.cerias.purdue.edu/pub/dict/wordlists/computer/Jargon.gz
Source14: http://ftp.cerias.purdue.edu/pub/dict/wordlists/computer/common-passwords.txt.gz
Source15: http://ftp.cerias.purdue.edu/pub/dict/wordlists/computer/etc-hosts.gz
Source16: http://ftp.cerias.purdue.edu/pub/dict/wordlists/movieTV/Movies.gz
Source17: http://ftp.cerias.purdue.edu/pub/dict/wordlists/movieTV/Python.gz
Source18: http://ftp.cerias.purdue.edu/pub/dict/wordlists/movieTV/Trek.gz
Source19: http://ftp.cerias.purdue.edu/pub/dict/wordlists/literature/LCarrol.gz
Source20: http://ftp.cerias.purdue.edu/pub/dict/wordlists/literature/Paradise.Lost.gz
Source21: http://ftp.cerias.purdue.edu/pub/dict/wordlists/literature/cartoon.gz
Source22: http://ftp.cerias.purdue.edu/pub/dict/wordlists/literature/myths-legends.gz
Source23: http://ftp.cerias.purdue.edu/pub/dict/wordlists/literature/sf.gz
Source24: http://ftp.cerias.purdue.edu/pub/dict/wordlists/literature/shakespeare.gz
Source25: http://ftp.cerias.purdue.edu/pub/dict/wordlists/names/ASSurnames.gz
Source26: http://ftp.cerias.purdue.edu/pub/dict/wordlists/names/Congress.gz
Source27: http://ftp.cerias.purdue.edu/pub/dict/wordlists/names/Family-Names.gz
Source28: http://ftp.cerias.purdue.edu/pub/dict/wordlists/names/Given-Names.gz
Source29: http://ftp.cerias.purdue.edu/pub/dict/wordlists/names/famous.gz
Source30: http://ftp.cerias.purdue.edu/pub/dict/wordlists/names/fast-names.gz
Source31: http://ftp.cerias.purdue.edu/pub/dict/wordlists/names/female-names.gz
Source32: http://ftp.cerias.purdue.edu/pub/dict/wordlists/names/male-names.gz
Source33: http://ftp.cerias.purdue.edu/pub/dict/wordlists/names/names.french.gz
Source34: http://ftp.cerias.purdue.edu/pub/dict/wordlists/names/names.hp.gz
Source35: http://ftp.cerias.purdue.edu/pub/dict/wordlists/names/other-names.gz
Source36: http://ftp.cerias.purdue.edu/pub/dict/wordlists/names/surnames.finnish.gz

# No upstream source for this; it came in as a bugzilla attachment.
Source37: pass_file.gz
# https://bugzilla.redhat.com/show_bug.cgi?id=557592
# https://bugzilla.redhat.com/attachment.cgi?id=386022
Source38: ry-threshold10.txt
Patch1: cracklib-2.8.15-inttypes.patch
Patch2: cracklib-2.8.12-gettext.patch
URL: http://sourceforge.net/projects/cracklib/
License: LGPLv2+
Buildroot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: python-devel, words, autoconf, automake, gettext, libtool
BuildRequires: gettext-autopoint
Conflicts: cracklib-dicts < 2.8
# The cracklib-format script calls gzip, but without a specific path.
Requires: gzip

%description
CrackLib tests passwords to determine whether they match certain
security-oriented characteristics, with the purpose of stopping users
from choosing passwords that are easy to guess. CrackLib performs
several tests on passwords: it tries to generate words from a username
and gecos entry and checks those words against the password; it checks
for simplistic patterns in passwords; and it checks for the password
in a dictionary.

CrackLib is actually a library containing a particular C function
which is used to check the password, as well as other C
functions. CrackLib is not a replacement for a passwd program; it must
be used in conjunction with an existing passwd program.

Install the cracklib package if you need a program to check users'
passwords to see if they are at least minimally secure. If you install
CrackLib, you will also want to install the cracklib-dicts package.

%package devel
Summary: Development files needed for building applications which use cracklib
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The cracklib-devel package contains the header files and libraries needed
for compiling applications which use cracklib.

%package python
Summary: Python bindings for applications which use cracklib
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description python
The cracklib-python package contains a module which permits applications
written in the Python programming language to use cracklib.

%package dicts
Summary: The standard CrackLib dictionaries
Group: System Environment/Libraries
BuildRequires: words >= 2-13
Requires: cracklib = %{version}-%{release}

%description dicts
The cracklib-dicts package includes the CrackLib dictionaries.
CrackLib will need to use the dictionary appropriate to your system,
which is normally put in /usr/share/dict/words. Cracklib-dicts also
contains the utilities necessary for the creation of new dictionaries.

If you are installing CrackLib, you should also install cracklib-dicts.

%prep
%setup -q -a 2
cp lib/packer.h lib/packer.h.in
# Replace zn_CN.po with one that wasn't mis-transcoded at some point.
grep '????????????????' po/zh_CN.po
install -p -m 644 %{SOURCE3} po/zh_CN.po
%patch1 -p1 -b .inttypes
%patch2 -p1 -b .gettext
autoreconf -f -i
mkdir cracklib-dicts
for dict in %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} %{SOURCE14} \
            %{SOURCE15} %{SOURCE16} %{SOURCE17} %{SOURCE18} %{SOURCE19} \
            %{SOURCE20} %{SOURCE21} %{SOURCE22} %{SOURCE23} %{SOURCE24} \
            %{SOURCE25} %{SOURCE26} %{SOURCE27} %{SOURCE28} %{SOURCE29} \
            %{SOURCE30} %{SOURCE31} %{SOURCE32} %{SOURCE33} %{SOURCE34} \
            %{SOURCE35} %{SOURCE36} %{SOURCE37} %{SOURCE38} %{SOURCE1}
do
        cp -fv ${dict} cracklib-dicts/
done
chmod +x util/cracklib-format

%build
%configure --with-pic --with-python --with-default-dict=%{dictpath} --disable-static
make

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -c -p" -C python
./util/cracklib-format cracklib-dicts/* | \
./util/cracklib-packer $RPM_BUILD_ROOT/%{dictpath}
./util/cracklib-format $RPM_BUILD_ROOT/%{dictdir}/cracklib-small | \
./util/cracklib-packer $RPM_BUILD_ROOT/%{dictdir}/cracklib-small
rm -f $RPM_BUILD_ROOT/%{dictdir}/cracklib-small
sed s,/usr/lib/cracklib_dict,%{dictpath},g lib/crack.h > $RPM_BUILD_ROOT/%{_includedir}/crack.h
ln -s cracklib-format $RPM_BUILD_ROOT/%{_sbindir}/mkdict
ln -s cracklib-packer $RPM_BUILD_ROOT/%{_sbindir}/packer
touch $RPM_BUILD_ROOT/top

toprelpath=..
touch $RPM_BUILD_ROOT/top
while ! test -f $RPM_BUILD_ROOT/%{_libdir}/$toprelpath/top ; do
	toprelpath=../$toprelpath
done
rm -f $RPM_BUILD_ROOT/top
if test %{dictpath} != %{_libdir}/cracklib_dict ; then
ln -s $toprelpath%{dictpath}.hwm $RPM_BUILD_ROOT/%{_libdir}/cracklib_dict.hwm
ln -s $toprelpath%{dictpath}.pwd $RPM_BUILD_ROOT/%{_libdir}/cracklib_dict.pwd
ln -s $toprelpath%{dictpath}.pwi $RPM_BUILD_ROOT/%{_libdir}/cracklib_dict.pwi
fi
rm -f $RPM_BUILD_ROOT/%{_libdir}/python*/site-packages/_cracklibmodule.*a
rm -f $RPM_BUILD_ROOT/%{_libdir}/libcrack.la

mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man{3,8}
install -p -m644 debian/*.3 $RPM_BUILD_ROOT/%{_mandir}/man3/
install -p -m644 debian/*.8 $RPM_BUILD_ROOT/%{_mandir}/man8/

%find_lang %{name}

%check
# We want to check that the new library is able to open the new dictionaries,
# using the new python module.
LD_LIBRARY_PATH=$RPM_BUILD_ROOT/%{_libdir} %{__python} 2>&1 << EOF
import string, sys
# Prepend buildroot-specific variations of the python path to the python path.
syspath2=[]
for element in sys.path:
	syspath2.append("$RPM_BUILD_ROOT/" + element)
syspath2.reverse()
for element in syspath2:
	sys.path.insert(0,element)
# Now actually do the test.  If we get a different result, or throw an
# exception, the script will end with the error.
import cracklib
try:
	s = cracklib.FascistCheck("cracklib", "$RPM_BUILD_ROOT/%{dictpath}")
except ValueError, message:
	expected = "it is based on a dictionary word"
	if message != expected:
		print "Got unexpected result \"%s\"," % messgae,
		print "instead of expected value of \"%s\"." % expected
		sys.exit(1)
	print "Got expected result \"%s\"," % message
	sys.exit(0)
finally:
	sys.exit(0)
EOF

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%triggerpostun -p /sbin/ldconfig -- cracklib < 2.7-24

%files -f %{name}.lang
%defattr(-,root,root)
%doc README README-WORDS NEWS README-LICENSE AUTHORS COPYING.LIB
%{_libdir}/libcrack.so.*
%dir %{_datadir}/cracklib
%{_datadir}/cracklib/cracklib.magic
%{_sbindir}/*cracklib*
%{_mandir}/man8/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libcrack.so
%{_mandir}/man3/*

%files dicts
%defattr(-,root,root)
%dir %{_datadir}/cracklib
%{_datadir}/cracklib/pw_dict.*
%{_datadir}/cracklib/cracklib-small.*
%{_libdir}/cracklib_dict.*
%{_sbindir}/mkdict
%{_sbindir}/packer

%files python
%defattr(-,root,root)
%{_libdir}/python*/site-packages/_cracklibmodule.so
%{_libdir}/../lib/python*/site-packages/*.py*

%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 2.8.18-4
- 为 Magic 3.0 重建

