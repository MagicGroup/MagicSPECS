%global gem_name mobileesp_converted

Name: rubygem-%{gem_name}
Version: 0.2.3
Release: 5%{?dist}
Summary: Provides device type detection based on HTTP request headers
Group: Development/Languages
License: ASL 2.0 
URL: http://github.com/jistr/mobileesp_converted
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems) 
BuildRequires: ruby(release)
BuildRequires: rubygems-devel 
BuildRequires: ruby 
#tests
BuildRequires: rubygem(rake)
BuildRequires: rubygem(minitest)

BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Autoconverted version (from Java to Ruby) of MobileESP library.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

sed -i '1{/#\!\/usr\/bin\/env rake/d}' %{buildroot}%{gem_instdir}/Rakefile

rm %{buildroot}%{gem_instdir}/.gitignore

%check
pushd .%{gem_instdir}
sed -i '/require "bundler\/gem_tasks"/d' ./Rakefile
rake test
popd


%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/LICENSE

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%{gem_instdir}/convert_to_ruby.vim
%{gem_instdir}/java_source/
%{gem_instdir}/spec/
%{gem_instdir}/%{gem_name}.gemspec

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.2.3-5
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.2.3-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Dec 16 2013 Miroslav Suchý <msuchy@redhat.com> 0.2.3-1
- rebase to mobileesp_converted-0.2.3

* Mon Aug 19 2013 Miroslav Suchý <msuchy@redhat.com> 0.2.2-1
- add license
- rebase to 0.2.2

* Mon Aug 05 2013 Miroslav Suchý <msuchy@redhat.com> 0.2.1-6
- 988310 - move bundler removal into %%check

* Mon Aug 05 2013 Miroslav Suchý <msuchy@redhat.com> 0.2.1-5
- 988310 - keep original gemspec in -doc subpackage
- 988310 - do not require bundler
- 988310 - remove shebang from non-executable Rakefile
- 988310 - remove not used code

* Thu Jul 25 2013 Miroslav Suchý <msuchy@redhat.com> 0.2.1-4
- add BR rubygem(bundler)

* Thu Jul 25 2013 Miroslav Suchý <msuchy@redhat.com> 0.2.1-3
- include gemspec (msuchy@redhat.com)
- use rake instead of rspec (msuchy@redhat.com)
- BR rubygem(minitest) (msuchy@redhat.com)
- enable tests (msuchy@redhat.com)

* Tue Jul 23 2013 Miroslav Suchý <msuchy@redhat.com> 0.2.1-2
- initial package

