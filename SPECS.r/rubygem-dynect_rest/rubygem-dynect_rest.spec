# Generated from dynect_rest-0.4.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name dynect_rest
%global rubyabi 1.9.1

Name:           rubygem-%{gem_name}
Version:        0.4.3
Release:        7%{?dist}
Summary:        Dynect REST API library

Group:          Development/Languages

License:        ASL 2.0
URL:            http://github.com/adamhjk/dynect_rest
Source0:        http://rubygems.org/gems/%{gem_name}-%{version}.gem

BuildArch:      noarch
Requires: ruby(release)
BuildRequires: ruby(release)
BuildRequires:  rubygems-devel
BuildRequires:  ruby
Requires:       ruby(rubygems)
Requires:       ruby
Requires:       rubygem(rest-client)
Requires:       rubygem(json)
Requires:       rubygem(json)
Requires:       rubygem(rest-client)
Provides:       rubygem(%{gem_name}) = %{version}

%description
Use the Dynect services REST API

%package doc
Summary:    Documentation for %{name}
Group:      Documentation
Requires:   %{name} = %{version}-%{release}
BuildArch:  noarch

%description doc
Documentation for %{name}

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
mkdir -p .%{gem_dir}

# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

# gem install installs into a directory.  We set that to be a local
# directory so that we can move it into the buildroot in install
gem install -V \
        --local \
        --install-dir ./%{gem_dir} \
        --force \
        --rdoc \
        %{gem_name}-%{version}.gem

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

rm -f %{buildroot}%{gem_instdir}/.document
rm -f %{buildroot}%{gem_instdir}/.rspec

%files
%dir %{gem_instdir}
%{gem_libdir}
%{gem_instdir}/spec
%{gem_instdir}/dynect_rest.gemspec
%{gem_instdir}/Gemfile*
%{gem_instdir}/Rakefile

%{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/example.rb
%doc %{gem_instdir}/VERSION

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.4.3-7
- 为 Magic 3.0 重建

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 14 2013 Russell Harrison <rharrison@fedoraproject.org> 0.4.3-5
- Update for Ruby 2.0 in F19+

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 29 2012 Russell Harrison <rharriso@redhat.com> 0.4.3-2
- Update spec to the new Ruby Packaging Guidelines

* Thu Apr 13 2012 Russell Harrison <rharriso@redhat.com> 0.4.3-1
- Update to 0.4.3

* Thu Mar 29 2012 Russell Harrison <rharriso@redhat.com> 0.4.1-1
- Update to 0.4.1

* Wed Feb 15 2012 Russell Harrison <rharriso@redhat.com> - 0.4.0-3
- Rebuilding with doc subpackage per package review.

* Wed Feb 15 2012 Russell Harrison <rharriso@redhat.com> - 0.4.0-2
- Changes for issues discussed in package review bug 790525

* Tue Feb 14 2012 Russell Harrison <rharriso@redhat.com> - 0.4.0-1
- Initial package
