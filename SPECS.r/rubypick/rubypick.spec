Summary: Stub to allow choosing Ruby runtime
Name: rubypick
Version: 1.1.0
Release: 1%{?dist}
License: MIT
URL: https://github.com/bkabrda/rubypick
Source0: https://github.com/bkabrda/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Requires: ruby(runtime_executable)
BuildArch: noarch

%description
Fedora /usr/bin/ruby stub to allow choosing Ruby runtime. Similarly to rbenv
or RVM, it allows non-privileged user to choose which is preferred Ruby
runtime for current task.

%prep
%setup -q


%build
# Nothing to do here.

%install
mkdir -p %{buildroot}%{_bindir}
cp -a ruby %{buildroot}%{_bindir}


%files
%doc README.md LICENSE
%{_bindir}/ruby


%changelog
* Wed Feb 20 2013 Vít Ondruch <vondruch@redhat.com> - 1.1.0-1
- Update to rubypick 1.1.0.

* Wed Feb 06 2013 Vít Ondruch <vondruch@redhat.com> - 1.0.2-3
- Simplified source URL, since GH now provides tarball that better fits to
  RPM build.

* Mon Feb 04 2013 Vít Ondruch <vondruch@redhat.com> - 1.0.2-2
- Add dependency on some Ruby executable.

* Mon Feb 04 2013 Vít Ondruch <vondruch@redhat.com> - 1.0.2-2
- Initial package.
