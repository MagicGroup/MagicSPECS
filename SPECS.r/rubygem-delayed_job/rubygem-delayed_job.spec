# Generated from delayed_job-2.1.3.gem by gem2rpm -*- rpm-spec -*-
%global gem_name delayed_job


Summary: Database-backed asynchronous priority queue system
Name: rubygem-%{gem_name}
Version: 4.0.6
Release: 3%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/collectiveidea/%{gem_name}
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(bundler) => 1.0.0
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(actionmailer) => 3.0.0
BuildRequires: rubygem(activerecord) => 3.0.0
BuildRequires: rubygem(sqlite3) => 1.3.0
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Delayed_job (or DJ) encapsulates the common pattern of asynchronously
executing longer tasks in the background. It is a direct extraction from
Shopify where the job table is responsible for a multitude of core tasks.
This gem is collectiveidea's fork
(http://github.com/collectiveidea/delayed_job).


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires:%{name} = %{version}-%{release}

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
# SimpleCov and Coverall are not necessary
sed -i "1,11d" spec/helper.rb
rspec spec
popd

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/LICENSE.md
%{gem_libdir}
%{gem_instdir}/contrib
%{gem_instdir}/recipes
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/CONTRIBUTING.md
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/Rakefile
%{gem_instdir}/spec


%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 4.0.6-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Feb 16 2015 Josef Stribny <jstribny@redhat.com> - 4.0.6-1
- Update to 4.0.6

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 02 2014 Josef Stribny <jstribny@redhat.com> - 4.0.1-1
- Update to delayed_job 4.0.1

* Mon Aug 12 2013 Josef Stribny <jstribny@redhat.com> - 4.0.0-1
- Update to delayed_job 4.0.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 11 2013 Vít Ondruch <vondruch@redhat.com> - 3.0.2-4
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 25 2012 Vít Ondruch <vondruch@redhat.com> - 3.0.2-1
- Update to delayed_job 3.0.2.

* Wed Feb 01 2012 Vít Ondruch <vondruch@redhat.com> - 2.1.4-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 22 2011 Vít Ondruch <vondruch@redhat.com> - 2.1.4-1
- Update to the delayed_job 2.1.4.

* Thu Feb 10 2011 Vít Ondruch <vondruch@redhat.com> - 2.1.3-1
- Initial package
