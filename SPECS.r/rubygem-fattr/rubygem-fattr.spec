%define gem_name fattr

Name:           rubygem-%{gem_name}
Summary:        Fatter attribute for Ruby
Version:        2.2.2
Release:        4%{?dist}
Group:          Development/Languages
License:        BSD or Ruby
URL:            https://github.com/ahoward/fattr
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem

BuildRequires:  ruby(release)
BuildRequires:  rubygems-devel
BuildRequires:  rubygem(test-unit)
BuildArch:      noarch

%description
The fattr gem is a Fatter attribute for Ruby

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


%check
pushd .%{gem_instdir}
ruby -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
popd

%files
%doc %{gem_docdir}
%doc %{gem_instdir}/LICENSE
%dir %{gem_instdir}/
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/Rakefile
%doc %{gem_instdir}/README
%doc %{gem_instdir}/README.erb
%doc %{gem_instdir}/samples
%doc %{gem_instdir}/test

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 2.2.2-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.2.2-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jul 08 2014 Vít Ondruch <vondruch@redhat.com> - 2.2.2-1
- Update to fattr 2.2.2.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 27 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.0-4
- F-19: Rebuild for ruby 2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 01 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 2.2.0-1
- Updated to 2.2.0 for rubygem-main to work properly.
- Introduced %%check section.
- Updated the license to BSD or Ruby.

* Thu Feb 02 2012 Vít Ondruch <vondruch@redhat.com> - 1.0.3-6
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Aug 13 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 1.0.3-3
- Really fix license
- Include license

* Wed Aug 05 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 1.0.3-2
- Fix license (Ruby)
- Fix URL

* Tue Jul 28 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 1.0.3-1
- First build of this package
