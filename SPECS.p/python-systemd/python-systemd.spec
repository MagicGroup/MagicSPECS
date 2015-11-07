Name:           python-systemd
Version:        230
Release:        3%{?dist}
Summary:        Python module wrapping systemd functionality

License:        LGPLv2+
URL:            https://github.com/systemd/python-systemd
#Source0:        https://github.com/systemd/python-systemd/archive/v%%{version}.tar.gz
# 'make dist' output from https://github.com/systemd/python-systemd/
Source0:        python-systemd-%{version}.tar.gz

BuildRequires:  systemd-devel
BuildRequires:  python2-devel
BuildRequires:  web-assets-devel
Requires:       js-jquery

Provides:       systemd-python = %{version}-%{release}
Provides:       systemd-python%{?_isa} = %{version}-%{release}
Obsoletes:      systemd-python < 230

%global _docdir_fmt %{name}

%description
Python module for native access to the systemd facilities.
Functionality includes sending of structured messages to the journal
and reading journal files, querying machine and boot identifiers and a
lists of message identifiers provided by systemd. Other functionality
provided by libsystemd is also wrapped.

This is the version for Python 2.

%package -n python3-systemd
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-sphinx

Provides:       systemd-python3 = %{version}-%{release}
Provides:       systemd-python3%{?_isa} = %{version}-%{release}
Obsoletes:      systemd-python3 < 230

%description -n python3-systemd
Python module for native access to the systemd facilities.
Functionality includes sending of structured messages to the journal
and reading journal files, querying machine and boot identifiers and a
lists of message identifiers provided by systemd. Other functionality
provided by libsystemd is also wrapped.

This is the version for Python 3.

%prep
%autosetup

%build
make PYTHON=%{__python2} build
make PYTHON=%{__python3} build
make PYTHON=%{__python3} SPHINX_BUILD=sphinx-build-3 sphinx-html
rm -r build/html/.buildinfo build/html/.doctrees

%install
%make_install PYTHON=%{__python2}
%make_install PYTHON=%{__python3}
mkdir -p %{buildroot}%{_pkgdocdir}
cp -rv build/html %{buildroot}%{_pkgdocdir}/
ln -vsf %{_jsdir}/jquery/latest/jquery.min.js %{buildroot}%{_pkgdocdir}/html/_static/jquery.js
cp README.md %{buildroot}%{_pkgdocdir}

%files
%license LICENSE.txt
%doc %{_pkgdocdir}
%{python2_sitearch}/*

%files -n python3-systemd
%license LICENSE.txt
%doc %{_pkgdocdir}
%{python3_sitearch}/*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 230-3
- 为 Magic 3.0 重建

* Wed Sep 30 2015 Liu Di <liudidi@gmail.com> - 230-2
- 为 Magic 3.0 重建

* Mon Jul  6 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@laptop> - 230-1
- Initial packaging
