%global gem_name require_all

Name:          rubygem-%{gem_name}
Version:       1.3.2
Release:       4%{?dist}
Summary:       A wonderfully simple way to load your code
Group:         Development/Languages
License:       MIT
URL:           http://github.com/jarmo/require_all
Source0:       https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires:      rubygems
BuildRequires: ruby
BuildRequires: rubygems-devel
# For Testing
BuildRequires: rubygem(rspec) => 2.14
BuildRequires: rubygem(simplecov) => 0.7
BuildRequires: rubygem(coveralls)
BuildArch:     noarch

%description
A wonderfully simple way to load your code.

Tired of futzing around with require statements everywhere,
littering your code with require File (__FILE__) crap? 
What if you could just point something at a big directory full 
of code and have everything just auto-magically load regardless 
of the dependency structure?

Wouldn't that be nice? Well, now you can!


%package doc
Summary:   Documentation for %{name}
Group:     Documentation
Requires:  %{name} = %{version}-%{release}
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
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# Cleanup
rm -rf %{buildroot}%{gem_instdir}/{.gitignore,.travis.yml,.yard*}
sed -i 's/\r$//' %{buildroot}%{gem_instdir}/{CHANGES,LICENSE,README.md}

# Run the test suite
%check
pushd .%{gem_instdir}
rspec -Ilib spec
popd

%files
%doc %{gem_instdir}/LICENSE
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/%{gem_name}.gemspec
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGES
%doc %{gem_instdir}/README.md
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%{gem_instdir}/spec

%changelog
* Wed Jul 09 2014 Troy Dawson <tdawson@redhat.com> - 1.3.2-4
- Minor spec tweaks

* Tue Jul 08 2014 Troy Dawson <tdawson@redhat.com> - 1.3.2-3
- Fix buildrequirements

* Mon Jul 07 2014 Troy Dawson <tdawson@redhat.com> - 1.3.2-2
- Enable tests

* Thu Jul 03 2014 Troy Dawson <tdawson@redhat.com> - 1.3.2-1
- Initial package
