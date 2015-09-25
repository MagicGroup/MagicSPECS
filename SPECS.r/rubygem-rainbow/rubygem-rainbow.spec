# Generated from rainbow-1.1.4.gem by gem2rpm -*- rpm-spec -*-
%global gem_name rainbow

Summary: Ruby String class extension enabling coloring text on ANSI terminals
Name: rubygem-%{gem_name}
Version: 2.0.0
Release: 4%{?dist}
Group: Development/Languages
License: MIT
URL: http://ku1ik.com/
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
# Test suite stopped to be part of the released .gem
# git clone https://github.com/sickill/rainbow.git && cd rainbow
# git checkout v2.0.0
# tar czvf rainbow-2.0.0-tests.tgz spec
Source1: rainbow-2.0.0-tests.tgz
Requires: ruby(release)
Requires: ruby(rubygems) 
BuildRequires: ruby(release)
BuildRequires: rubygems-devel 
BuildRequires: rubygem(rspec)
BuildRequires: ruby 
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Rainbow is an extension to the Ruby String class adding support for colorizing
text on ANSI terminals.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}

tar xzvf %{SOURCE1}
rspec spec

popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/%{gem_name}.gemspec
%exclude %{gem_instdir}/.travis.yml
%exclude %{gem_instdir}/.rubocop.yml
%exclude %{gem_instdir}/.gitignore
%{gem_spec}
%doc %{gem_instdir}/LICENSE

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.markdown
%doc %{gem_instdir}/Changelog.md
%{gem_instdir}/Gemfile
%{gem_instdir}/Guardfile
%{gem_instdir}/Rakefile
%{gem_instdir}/spec

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.0.0-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 07 2014 Josef Stribny <jstribny@redhat.com> - 2.0.0-1
- Update to rainbow 2.0.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 27 2013 Josef Stribny <jstribny@redhat.com> - 1.1.4-4
- F-19: Rebuild for ruby 2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 17 2012 Josef Stribny <jstribny@redhat.com> - 1.1.4-2
- Removed a patch for tests in %check, replaced by CLICOLOR_FORCE=1 instead

* Wed Dec 12 2012 Josef Stribny <jstribny@redhat.com> - 1.1.4-1
- Initial package
