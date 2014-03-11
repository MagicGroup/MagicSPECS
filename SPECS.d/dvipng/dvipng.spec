Name:           dvipng
Version:        1.14
Release:        2%{?dist}
Summary:        Converts DVI files to PNG/GIF format

Group:          Applications/Publishing 
License:        GPLv2+ and OFSFDL
URL:            http://savannah.nongnu.org/projects/dvipng/
Source0:        http://download.savannah.gnu.org/releases/dvipng/%{name}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  kpathsea-devel gd-devel zlib-devel libpng-devel texinfo-tex
BuildRequires:  t1lib-devel freetype-devel

Requires(pre):  /sbin/install-info 
Requires(post): /sbin/install-info

%description
This program makes PNG and/or GIF graphics from DVI files as obtained
from TeX and its relatives.

It is intended to produce anti-aliased screen-resolution images as
fast as is possible. The target audience is people who need to generate
and regenerate many images again and again. 

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'

rm -rf $RPM_BUILD_ROOT/%{_infodir}/dir

for i in ChangeLog ChangeLog.0 ; do
    iconv -f ISO-8859-1 -t UTF8 $i > $i.utf8 && touch -r $i $i.utf8 && mv $i.utf8 $i
done

%clean
rm -rf $RPM_BUILD_ROOT

%post 
/sbin/install-info %{_infodir}/dvipng.info %{_infodir}/dir 2>/dev/null || :

%preun
if [ "$1" = "0" ] ; then 
   /sbin/install-info --delete %{_infodir}/dvipng.info %{_infodir}/dir 2>/dev/null || :
fi

%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog ChangeLog.0 README RELEASE
%{_bindir}/dvigif
%{_bindir}/dvipng
%{_infodir}/dvipng.info*
%{_mandir}/man1/dvigif.1*
%{_mandir}/man1/dvipng.1*

%changelog
