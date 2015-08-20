Summary: The procmail mail processing program
Summary(zh_CN.UTF-8): procmail 邮件处理系统
Name: procmail
Version: 3.22
Release: 26%{?dist}
License: GPLv2+ or Artistic
Group: Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
Source: ftp://ftp.procmail.org/pub/procmail/procmail-%{version}.tar.gz
Source2: http://www.linux.org.uk/~telsa/BitsAndPieces/procmailrc
URL: http://www.procmail.org
Patch0: procmail-3.22-rhconfig.patch
Patch1: procmail-3.15.1-man.patch
Patch2: procmail_3.22-8.debian.patch
Patch4: procmail-3.22-truncate.patch
Patch5: procmail-3.22-ipv6.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Procmail can be used to create mail-servers, mailing lists, sort your
incoming mail into separate folders/files (real convenient when subscribing
to one or more mailing lists or for prioritising your mail), preprocess
your mail, start any programs upon mail arrival (e.g. to generate different
chimes on your workstation for different types of mail) or selectively
forward certain incoming mail automatically to someone.

%description -l zh_CN.UTF-8
Procmail 可以用来建立邮件服务，邮件列表，把你的邮件分拣到不同的文件夹，预
处理你的邮件，根据到达的邮件启动任何程序等等。

%prep
%setup -q
%patch0 -p1 -b .rhconfig
%patch1 -p1
%patch2 -p1
%patch4 -p1 -b .truncate
%patch5 -p1 -b .ipv6

sed -i 's/getline/get_line/g' src/fields.c \
                              src/formail.c \
                              src/formisc.c \
			      src/formisc.h

find examples -type f | xargs chmod 644

%build
make RPM_OPT_FLAGS="$(getconf LFS_CFLAGS)" autoconf.h
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS $(getconf LFS_CFLAGS)"

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man{1,5}

make \
    BASENAME=${RPM_BUILD_ROOT}%{_prefix} MANDIR=${RPM_BUILD_ROOT}%{_mandir} \
    install

cp debian/mailstat.1 ${RPM_BUILD_ROOT}%{_mandir}/man1
cp -p %{SOURCE2} telsas_procmailrc


%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%doc Artistic COPYING FAQ FEATURES HISTORY README KNOWN_BUGS examples telsas_procmailrc debian/QuickStart debian/README.Maildir

%{_bindir}/formail
%attr(2755,root,mail) %{_bindir}/lockfile
%{_bindir}/mailstat
%attr(0755,root,mail) %{_bindir}/procmail

%{_mandir}/man[15]/*

%changelog
* Tue Aug 04 2015 Liu Di <liudidi@gmail.com> - 3.22-26
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 3.22-25
- 为 Magic 3.0 重建

* Wed Jan 25 2012 Liu Di <liudidi@gmail.com> - 3.22-24
- 为 Magic 3.0 重建


