# Generated from jquery-ui-rails-5.0.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name jquery-ui-rails

Name: rubygem-%{gem_name}
Version: 5.0.0
Release: 4%{?dist}
Summary: jQuery UI packaged for the Rails asset pipeline
Group: Development/Languages
License: MIT
URL: https://github.com/joliss/jquery-ui-rails
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel >= 1.3.6
BuildRequires: ruby 
BuildArch: noarch

%description
jQuery UI's JavaScript, CSS, and image files packaged for the Rails 3.1+ asset
pipeline.


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


%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/.gitignore
%exclude %{gem_instdir}/.gitmodules
%exclude %{gem_instdir}/.travis.yml
%{gem_spec}
%license %{gem_instdir}/License.txt
%{gem_instdir}/app

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/VERSIONS.md
%doc %{gem_instdir}/History.md
%{gem_instdir}/Rakefile
%{gem_instdir}/Gemfile

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 5.0.0-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Sep 16 2014 Josef Stribny <jstribny@redhat.com> - 5.0.0-2
- Use new %%license macro

* Thu Jul 24 2014 Josef Stribny <jstribny@redhat.com> - 5.0.0-1
- Initial package
