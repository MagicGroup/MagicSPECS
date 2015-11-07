%global gem_name hoptoad_notifier

Name: rubygem-%{gem_name}
Version: 2.4.11
Release: 9%{?dist}
Summary: Send your application errors to our hosted service and reclaim your inbox
Group: Development/Languages
License: MIT 
URL: http://www.hoptoadapp.com
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems) 
Requires: rubygem(builder) 
Requires: rubygem(activesupport) 
BuildRequires: ruby(release)
BuildRequires: rubygems-devel 
BuildRequires: ruby 
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
This is the notifier plugin for integrating apps with Hoptoad.

When an uncaught exception occurs, HoptoadNotifier will POST the relevant data
to the Hoptoad server specified in your environment.


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
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/




%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%{gem_instdir}/generators/
%{gem_instdir}/script/
%{gem_instdir}/rails/
%doc %{gem_instdir}/INSTALL
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/MIT-LICENSE

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG
%doc %{gem_instdir}/README_FOR_HEROKU_ADDON.md
%doc %{gem_instdir}/TESTING.rdoc
%doc %{gem_instdir}/SUPPORTED_RAILS_VERSIONS
%{gem_instdir}/test/
%{gem_instdir}/Rakefile

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 2.4.11-9
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.4.11-8
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Aug 05 2013 Miroslav Suchý <msuchy@redhat.com> 2.4.11-5
- 988789 - Description should end up with a dot.
- 988789 - move LICENSE to main package

* Fri Jul 26 2013 Miroslav Suchý <msuchy@redhat.com> 2.4.11-4
- set description

* Fri Jul 26 2013 Miroslav Suchý <msuchy@redhat.com> 2.4.11-3
- remove spec from files

* Thu Jul 25 2013 Miroslav Suchý <msuchy@redhat.com> 2.4.11-2
- initial package

* Thu Jul 25 2013 msuchy@redhat.com - 2.4.11-1
- Initial package
