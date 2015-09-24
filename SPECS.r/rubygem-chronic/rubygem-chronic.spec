# Generated from chronic-0.2.3.gem by gem2rpm -*- rpm-spec -*-

%global gem_name chronic

Summary: A natural language date parser
Name: rubygem-%{gem_name}
Version: 0.10.2
Release: 2%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/mojombo/chronic
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem

BuildRequires: ruby
BuildRequires: rubygems-devel
BuildRequires: rubygem(minitest) > 5
BuildArch: noarch

%description
Chronic is a natural language date/time parser written in pure Ruby.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires:%{name} = %{version}-%{release}

%description doc
Documentation for %{name}.

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
ruby -Itest -e 'Dir.glob "./test/**/test_*.rb", &method(:require)'
popd


%files
%exclude %{gem_instdir}/.*
%exclude %{gem_instdir}/%{gem_name}.gemspec
%dir %{gem_instdir}
%{gem_libdir}
%doc %{gem_instdir}/LICENSE
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/HISTORY.md
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/test

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jul 15 2014 Vít Ondruch <vondruch@redhat.com> - 0.10.2-1
- Update to Chronic 0.10.2.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 08 2013 Vít Ondruch <vondruch@redhat.com> - 0.9.1-1
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Update to Chronic 0.9.1.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 31 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.6.6-1
- Rebuilt for Ruby 1.9.3.
- Update to Chronic 0.6.6.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jun 29 2010 Shreyank Gupta <sgupta@redhat.com> - 0.2.3-2
- Added BR: rubygem(rake) and rubygem(hoe)
- Removed R: rubygem(hoe)
- Removed hoe depedency from specfile

* Fri Jun 18 2010 Shreyank Gupta <sgupta@redhat.com> - 0.2.3-1
- Initial package
