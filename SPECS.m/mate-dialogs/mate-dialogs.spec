Name:	mate-dialogs	
Version:	1.4.0
Release:	3%{?dist}
Summary:	Displays dialog boxes from shell scripts
License:	LGPLv2+ and GPLv2+
URL:		http://mate-desktop.org
Source0:	http://pub.mate-desktop.org/releases/1.4/%{name}-%{version}.tar.xz

BuildRequires:	gtk+-devel gtk2-devel mate-common mate-doc-utils rarian-compat 

%description
Displays dialog boxes from shell scripts.

%prep
%setup -q


%build
NOCONFIGURE=1 ./autogen.sh
%configure --disable-static --enable-libmatenotify

make %{?_smp_mflags} V=1


%install
make install DESTDIR=%{buildroot}
magic_rpm_clean.sh
%find_lang %{name}


%files -f %{name}.lang
%doc AUTHORS COPYING README
%{_bindir}/gdialog
%{_bindir}/matedialog
%{_mandir}/man1/*
%{_datadir}/mate/
%{_datadir}/omf/matedialog/
%{_datadir}/matedialog/

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.4.0-3
- 为 Magic 3.0 重建

* Sat Aug 11 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-2
- Remove unnecessary require fields, update description, make package own mate and matedialog datadirs and add V=1 to make field.

* Sun Aug 5 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-1
- Initial build
