# Generated from em-worker-0.0.2.gem by gem2rpm -*- rpm-spec -*-
%global gem_name em-worker

Name: rubygem-%{gem_name}
Version: 0.0.2
Release: 5%{?dist}
Summary: Provides a simple task worker, with a task concurrency limit
Group: Development/Languages
License: MIT
URL: https://github.com/portertech/em-worker
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem-rspec
BuildRequires: rubygem(eventmachine)
Requires: rubygems
%if 0%{?rhel} > 0
Provides: rubygem(%{gem_name}) = %{version}
%endif

BuildArch: noarch

%description
Provides a simple task worker, with a task concurrency limit.


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
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

rm -f %{buildroot}%{gem_instdir}/{.gitignore,.travis.yml,.rspec}


# Run the test suite
%check
pushd .%{gem_instdir}
rspec -Ilib spec
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%doc %{gem_instdir}/LICENSE.txt
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/Gemfile

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Rakefile
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/spec

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.0.2-5
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.0.2-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 24 2015 Graeme Gillies <ggillies@redhat.com> - 0.0.2-2
- Updated spec file to have base package correctly require rubygems
- Updated spec file to allow building for EPEL-7

* Thu Jan 29 2015 Graeme Gillies <ggillies@redhat.com> - 0.0.2-1
- Initial package
