Summary:	Archiver for .arj files
Summary(zh_CN):	.arj 文件的归档
Name:		arj
Version:	3.10.22
Release:	12%{?dist}
License:	GPL+
Group:		Applications/Archiving
Group(zh_CN):	应用程序/归档
URL:		http://arj.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# unarj.* from Debian
Source1:	unarj.sh
Source2:	unarj.1
Patch0:		http://ftp.debian.org/debian/pool/main/a/%{name}/%{name}_%{version}-6.diff.gz
Patch1:		arj-3.10.22-missing-protos.patch
Patch2:		arj-3.10.22-custom-printf.patch
BuildRequires:	autoconf
Provides:	unarj = %{version}-%{release}
Obsoletes:	unarj < 3
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
This package is an open source version of the arj archiver. It has
been created with the intent to preserve maximum compatibility and
retain the feature set of original ARJ archiver as provided by ARJ
Software, Inc.

%description -l zh_CN
这是压缩和解压 arj 文件命令的开放源码版本。

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

for i in debian/patches/00*.patch; do
  patch -p1 < $i
done

pushd gnu
  autoconf
popd

%build
pushd gnu
  %configure
popd

# Disable binary strippings
make %{?_smp_mflags} ADD_LDFLAGS=""

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

install -Dpm 644 resource/rearj.cfg.example $RPM_BUILD_ROOT%{_sysconfdir}/rearj.cfg
install -pm 755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/unarj
install -pm 644 %{SOURCE2} $RPM_BUILD_ROOT%{_mandir}/man1/unarj.1

# remove the register remainders of arj's sharewares time
rm -f $RPM_BUILD_ROOT%{_bindir}/arj-register
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/arj-register.1*

magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc ChangeLog* doc/COPYING doc/rev_hist.txt
%config(noreplace) %{_sysconfdir}/rearj.cfg
%{_bindir}/*arj*
%{_libdir}/arj/
%{_mandir}/man1/*arj*1.*

%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 3.10.22-12
- 为 Magic 3.0 重建

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 3.10.22-10
- 为 Magic 3.0 重建

* Sun Oct 30 2011 Liu Di <liudidi@gmail.com> - 3.10.22-9
- 为 Maigc 3.0 重建
