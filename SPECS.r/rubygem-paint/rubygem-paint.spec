%global gem_name paint

Name: rubygem-%{gem_name}
Version: 1.0.0
Release: 4%{?dist}
Summary: Terminal painter
Group: Development/Languages
License: MIT
URL: https://github.com/janlelis/paint
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel 
BuildArch: noarch
#tests
BuildRequires: rubygem(rspec-core)

%description
Paint manages terminal colors and effects for you. It combines the strengths
of term-ansicolor, rainbow and other similar projects into a simple to use,
however still flexible terminal colorization gem with no core extensions by
default.


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

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/
rm %{buildroot}%{gem_instdir}/{.travis.yml,.rspec}

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%exclude %{gem_instdir}/.gemtest
%doc %{gem_instdir}/README.rdoc
%license %{gem_instdir}/MIT-LICENSE.txt

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.rdoc
%{gem_instdir}/Rakefile
%{gem_instdir}/%{gem_name}.gemspec

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 1.0.0-4
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.0.0-3
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.0.0-2
- 为 Magic 3.0 重建

* Fri Jun 19 2015 Miroslav Suchý <msuchy@redhat.com> 1.0.0-1
- rebase to paint-1.0.0

* Tue Nov 25 2014 Miroslav Suchý <miroslav@suchy.cz> 0.9.0-2
- rebase to 0.9.0

* Tue Jan 21 2014 Miroslav Suchý <miroslav@suchy.cz> 0.8.7-1
- rebase paint-0.8.7.gem

* Mon Aug 26 2013 Miroslav Suchý <msuchy@redhat.com> 0.8.6-3
- 998459 - move README and LICENSE to main package
- 998459 - remove excessive cp
- 998459 - use virtual requires
- 998459 - remove ruby mri requires

* Mon Aug 19 2013 Miroslav Suchý <msuchy@redhat.com> 0.8.6-2
- enable tests
- fix files section

* Mon Aug 19 2013 Miroslav Suchý <msuchy@redhat.com> 0.8.6-1
- initial package

