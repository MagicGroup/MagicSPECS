%global gem_name gssapi

Name: rubygem-%{gem_name}
Version: 1.2.0
Release: 3%{?dist}
Summary: A FFI wrapper around the system GSSAPI library
Group: Development/Languages
License: MIT
URL: http://github.com/zenchild/gssapi
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems)
Requires: rubygem(ffi) >= 1.0.1
Requires: krb5-libs
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 1.8.7
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
A FFI wrapper around the system GSSAPI library. Please make sure and read
the Yard docs or standard GSSAPI documentation if you have any questions.
There is also a class called GSSAPI::Simple that wraps many of the common
features used for GSSAPI.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/
rm -f %{buildroot}%{gem_instdir}/%{gem_name}.gemspec


%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%doc %{gem_instdir}/COPYING

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/COPYING
%doc %{gem_instdir}/Changelog.md
%doc %{gem_instdir}/Gemfile
%{gem_instdir}/VERSION
%{gem_instdir}/examples
%{gem_instdir}/test
%{gem_instdir}/Rakefile
%doc %{gem_instdir}/preamble

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.2.0-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Sep 22 2014 <jpazdziora@redhat.com> - 1.2.0-1
- 1145033 - rebased to gssapi-1.2.0.gem.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 04 2013 Jan Pazdziora <jpazdziora@redhat.com> - 1.1.2-2
- 981119 - adding dependence on krb5-libs which provides the .so.

* Mon Jun 24 2013 Jan Pazdziora <jpazdziora@redhat.com> - 1.1.2-1
- Initial package
