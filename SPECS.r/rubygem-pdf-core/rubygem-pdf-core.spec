%global gem_name pdf-core

Name: rubygem-%{gem_name}
Version: 0.6.0
Release: 4%{?dist}
Summary: PDF::Core is used by Prawn to render PDF documents
Group: Development/Languages
License: GPLv2 or GPLv3 or Ruby 
URL: http://prawn.majesticseacreature.com
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Relax pdf-reader to < 1.3.4 to match what we have in Fedora
Patch0: pdf-core-0.2.5-relax-pdf-reader.patch
BuildRequires: ruby(release)
BuildRequires: rubygems-devel >= 1.3.6
BuildRequires: ruby >= 1.9.3
BuildRequires: rubygem(pdf-inspector) >= 1.1.0
BuildRequires: rubygem(pdf-reader) >= 1.2
BuildRequires: rubygem(pdf-reader) < 1.3.4
BuildRequires: rubygem(rspec)
BuildArch: noarch

%description
PDF::Core is used by Prawn to render PDF documents.


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
%patch0 -p1

%build
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


%check
pushd .%{gem_instdir}
# get rid of bundler
sed -i -e 's/require "bundler"//' spec/spec_helper.rb
sed -i -e 's/Bundler.setup//' spec/spec_helper.rb
rspec spec
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/COPYING
%doc %{gem_instdir}/GPLv2
%doc %{gem_instdir}/GPLv3

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/spec

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 0.6.0-4
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.6.0-3
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.6.0-2
- 为 Magic 3.0 重建

* Mon Aug 24 2015 Josef Stribny <jstribny@redhat.com> - 0.6.0-1
- Update to 0.6.0

* Mon Jun 22 2015 Josef Stribny <jstribny@redhat.com> - 0.5.1-1
- Update to 0.5.1

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 05 2014 Josef Stribny <jstribny@redhat.com> - 0.2.5-1
- Initial package
