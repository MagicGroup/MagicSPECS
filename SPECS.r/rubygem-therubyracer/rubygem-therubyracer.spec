%global gem_name therubyracer

%global majorver 0.11.0
%global release 13
#%%global preminorver beta5
%global fullver %{majorver}%{?preminorver}

%{?preminorver:%global gem_instdir %{gem_dir}/gems/%{gem_name}-%{fullver}}
%{?preminorver:%global gem_extdir %{_libdir}/gems/exts/%{gem_name}-%{fullver}}
%{?preminorver:%global gem_docdir %{gem_dir}/doc/%{gem_name}-%{fullver}}
%{?preminorver:%global gem_spec %{gem_dir}/specifications/%{gem_name}-%{fullver}.gemspec}
%{?preminorver:%global gem_cache %{gem_dir}/cache/%{gem_name}-%{fullver}.gem}

Summary: Embed the V8 Javascript interpreter into Ruby
Name: rubygem-%{gem_name}
Version: %{majorver}
Release: %{?preminorver:0.}%{release}%{?preminorver:.%{preminorver}}%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/cowboyd/therubyracer
Source0: http://rubygems.org/gems/%{gem_name}-%{version}%{?preminorver}.gem
Patch0: %{name}-0.11.1-fix-bignum-conversion.patch
Patch1: rubygem-therubyracer-0.11.0beta5-v8-3.14.5.8-compatibility.patch
Requires: v8
BuildRequires: ruby(release)
BuildRequires: rubygem(ref)
%if 0%{?fedora} >= 22
BuildRequires: rubygem(rspec2)
%else
BuildRequires: rubygem(rspec)
%endif
BuildRequires: rubygems-devel
BuildRequires: ruby-devel
BuildRequires: v8-devel
# some specs run "ps aux"
BuildRequires: /usr/bin/ps
# same as in v8
ExclusiveArch:  %{ix86} x86_64 %{arm}

%description
Call javascript code and manipulate javascript objects from ruby. Call ruby
code and manipulate ruby objects from javascript.


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

%patch0 -p1
%patch1 -p1

%build
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{gem_extdir_mri}/v8
cp -a .%{gem_extdir_mri}/gem.build_complete %{buildroot}%{gem_extdir_mri}/
cp -a .%{gem_extdir_mri}/v8/*.so %{buildroot}%{gem_extdir_mri}/v8/

# Remove the binary extension sources and build leftovers.
rm -rf %{buildroot}%{gem_instdir}/ext

# remove shebang in non-executable file
sed -i '1d' %{buildroot}%{gem_instdir}/Rakefile

%check
pushd .%{gem_instdir}
# this spec doesn't test anything, only requires redjs, which is not in fedora
mv spec/redjs_spec.rb spec/redjs_spec.rb.notest

# fix the v8 version we're testing against
V8_VERSION=`d8 -e "print(version())"`
sed -i "s|V8::C::V8::GetVersion().*|V8::C::V8::GetVersion().should match /^${V8_VERSION}/|" spec/c/constants_spec.rb

# skip the threading specs for now
# https://github.com/cowboyd/therubyracer/pull/98#issuecomment-14442089
%if 0%{?fedora} >= 22
rspec2 \
%else
rspec \
%endif
	-I$(dirs +1)%{gem_extdir_mri} spec --tag ~threads
popd

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/README.md
%{gem_libdir}
%{gem_extdir_mri}
%exclude %{gem_cache}
%exclude %{gem_instdir}/.*
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/Changelog.md
%{gem_instdir}/benchmarks.rb
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%{gem_instdir}/spec
%{gem_instdir}/thefrontside.png
%{gem_instdir}/therubyracer.gemspec

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 0.11.0-13
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.11.0-12
- 为 Magic 3.0 重建

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.11.0-10
- Rebuilt for GCC 5 C++11 ABI change

* Mon Jan 19 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.11.0-9
- Use rspec 2 for now

* Sun Jan 18 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.11.0-8
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_2.2

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.0-7.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.0-6.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 15 2014 Josef Stribny <jstribny@redhat.com> - 0.11.0-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Fri Feb 14 2014 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.11.0-4
- rebuild for icu-53 (via v8)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.11.0-2
- Add patch that fixes bignum operations on Ruby 2.0.

* Thu Mar 07 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.11.0-1
- Updated to 0.11.0 final.

* Thu Feb 28 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.11.0-0.6.beta5
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.0-0.5.beta5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 09 2013 Dan Horák <dan[at]danny.cz> - 0.11.0-0.4.beta5
- supported arch list set to match v8

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.0-0.3.beta5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.11.0-0.2.beta5
- Fixed minor issues according to review comments (RHBZ #838870).

* Fri Jun 15 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.11.0-0.1.beta5
- Initial package
