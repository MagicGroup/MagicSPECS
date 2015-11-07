Summary: Stub to allow choosing Ruby runtime
Name: rubypick
Version: 1.1.1
Release: 6%{?dist}
License: MIT
URL: https://github.com/bkabrda/rubypick
Source0: https://github.com/bkabrda/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Requires: ruby(runtime_executable)
# Hint DNF that MRI is preferred interpreter.
Suggests: ruby
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
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.1.1-6
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.1.1-5
- 为 Magic 3.0 重建

* Wed Jul 22 2015 Vít Ondruch <vondruch@redhat.com> - 1.1.1-4
- Use MRI by default.

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jan 20 2014 Vít Ondruch <vondruch@redhat.com> - 1.1.1-1
- Update to rubypick 1.1.1.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 20 2013 Vít Ondruch <vondruch@redhat.com> - 1.1.0-1
- Update to rubypick 1.1.0.

* Wed Feb 06 2013 Vít Ondruch <vondruch@redhat.com> - 1.0.2-3
- Simplified source URL, since GH now provides tarball that better fits to
  RPM build.

* Mon Feb 04 2013 Vít Ondruch <vondruch@redhat.com> - 1.0.2-2
- Add dependency on some Ruby executable.

* Mon Feb 04 2013 Vít Ondruch <vondruch@redhat.com> - 1.0.2-2
- Initial package.
