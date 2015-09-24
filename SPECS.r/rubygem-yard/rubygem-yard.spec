%global gem_name yard

Name: rubygem-%{gem_name}
Version: 0.8.7.6
Release: 1%{?dist}
Summary: Documentation tool for consistent and usable documentation in Ruby
Group: Development/Languages
License: MIT and (BSD or Ruby)
URL: http://yardoc.org
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(RedCloth)
BuildRequires: rubygem(rspec) < 3
BuildRequires: rubygem(redcarpet)
BuildRequires: rubygem(rack)
BuildArch: noarch

%description
YARD is a documentation generation tool for the Ruby programming language.
It enables the user to generate consistent, usable documentation that can be
exported to a number of formats very easily, and also supports extending for
custom Ruby constructs such as custom class level definitions.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -T -c
%gem_install -n %{SOURCE0}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

%check
pushd .%{gem_instdir}
# Not sure if this is needed, since bundler is not user or because Fedora
# provides more recent RSpec :/
sed -i '/File\.stub(:exist?).with(\/\\\.yardopts$\/)/ i\      File.stub(:exist?).and_return(true)' spec/cli/server_spec.rb

rspec2 spec
popd

%files
%{_bindir}/yardoc
%{_bindir}/yri
%{_bindir}/yard
%dir %{gem_instdir}
%{gem_instdir}/bin
%{gem_libdir}
%{gem_instdir}/templates
%exclude %{gem_instdir}/.yardopts
%doc %{gem_instdir}/LEGAL

%exclude %{gem_cache}
%{gem_spec}

%license %{gem_instdir}/LICENSE

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/benchmarks
%{gem_instdir}/spec
%doc %{gem_instdir}/docs



%changelog
* Wed Jul 08 2015 Vít Ondruch <vondruch@redhat.com> - 0.8.7.6-1
- Update to YARD 0.8.7.6.

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jul 03 2014 Vít Ondruch <vondruch@redhat.com> - 0.8.7.4-1
- Update to yard 0.8.7.4.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug 14 2013 Vít Ondruch <vondruch@redhat.com> - 0.8.7-1
- Update to yard 0.8.7.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 15 2013 Vít Ondruch <vondruch@redhat.com> - 0.8.5.2-1
- Update to yard 0.8.5.2.

* Fri Mar 15 2013 Vít Ondruch <vondruch@redhat.com> - 0.8.2.1-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 27 2012 Vít Ondruch <vondruch@redhat.com> - 0.8.2.1-1
- Update to yard 0.8.2.1.

* Thu May 03 2012 Vít Ondruch <vondruch@redhat.com> - 0.8.1-1
- Update to yard 0.8.1.

* Wed Jan 25 2012 Vít Ondruch <vondruch@redhat.com> - 0.7.4-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 15 2011 Vít Ondruch <vondruch@redhat.com> - 0.7.4-1
- Updated to yard 0.7.4.

* Mon Jul 25 2011 Mo Morsi <mmorsi@redhat.com> - 0.7.2-1
- update to latest upstream release
- fixes to conform to fedora guidelines

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 22 2010 Mohammed Morsi <mmorsi@redhat.com> - 0.5.3-3
- fixed dependencies/package issues according to guidelines

* Mon Feb 08 2010 Mohammed Morsi <mmorsi@redhat.com> - 0.5.3-2
- cleaned up macros, other package guideline compliance fixes
- corrected license, added MIT
- include all files and docs, added check/test section

* Mon Feb 08 2010 Mohammed Morsi <mmorsi@redhat.com> - 0.5.3-1
- Initial package

