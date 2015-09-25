%global	gem_name	unf_ext
%if		0%{?fedora} < 19
%global	rubyabi	1.9.1
%endif

Summary:	Unicode Normalization Form support library for CRuby
Name:		rubygem-%{gem_name}
Version:	0.0.7.1
Release:	3%{?dist}

Group:		Development/Languages
# LICENSE.txt
License:	MIT
URL:		http://github.com/knu/ruby-unf_ext
Source0:	http://rubygems.org/gems/%{gem_name}-%{version}.gem

%if 0%{?fedora} >= 19
Requires:	ruby(release)
BuildRequires:	ruby(release)
%else
Requires:	ruby(abi) = %{rubyabi}
Requires:	ruby
BuildRequires:	ruby(abi) = %{rubyabi}
BuildRequires:	ruby
%endif

Requires:	ruby(rubygems) 
BuildRequires:	rubygems-devel 
BuildRequires:	ruby-devel
# %%check
BuildRequires:	rubygem(test-unit)
Provides:	rubygem(%{gem_name}) = %{version}-%{release}

%description
Unicode Normalization Form support library for CRuby.


%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -c -T

TOPDIR=$(pwd)
mkdir tmpunpackdir
pushd tmpunpackdir

gem unpack %{SOURCE0}
cd %{gem_name}-%{version}

gem specification -l --ruby %{SOURCE0} > %{gem_name}.gemspec
gem build %{gem_name}.gemspec
mv %{gem_name}-%{version}.gem $TOPDIR

popd
rm -rf tmpunpackdir

%build
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

%if 0%{?fedora} >= 21
mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a ./%{gem_extdir_mri}/* %{buildroot}%{gem_extdir_mri}/

pushd %{buildroot}
rm -f .%{gem_extdir_mri}/{gem_make.out,mkmf.log}
popd

%else
mkdir -p %{buildroot}%{gem_extdir_mri}/lib
mv \
	%{buildroot}%{gem_libdir}/%{gem_name}.so \
	%{buildroot}%{gem_extdir_mri}/lib/

%endif

# Remove the binary extension sources and build leftovers.
rm -rf %{buildroot}%{gem_instdir}/ext
rm -f %{buildroot}%{gem_instdir}/{.document,.gitignore}
rm -f %{buildroot}%{gem_instdir}/.travis.yml

%check
pushd .%{gem_instdir}
sed -i.orig \
	-e '/begin/,/end/d' \
	-e '/bundler/d' \
	test/helper.rb

sed -i -e '2i gem "test-unit"' test/helper.rb

ruby \
%if 0%{?fedora} >= 21
	-Ilib:test:.:ext/%{gem_name} \
%else
	-Ilib:test \
%endif
test/test_unf_ext.rb

%files
%dir	%{gem_instdir}
%doc	%{gem_instdir}/[A-Z]*
%exclude	%{gem_instdir}/Gemfile
%exclude	%{gem_instdir}/Rakefile
%exclude	%{gem_instdir}/*.gemspec

%dir	%{gem_libdir}
%{gem_libdir}/%{gem_name}.rb
%{gem_libdir}/%{gem_name}/

%if 0%{?fedora} >= 21
%{gem_extdir_mri}/
%else
%dir	%{gem_extdir_mri}
%dir	%{gem_extdir_mri}/lib
%{gem_extdir_mri}/lib/%{gem_name}.so
%endif

%exclude	%{gem_cache}
%{gem_spec}

%files doc
%doc	%{gem_docdir}
%exclude	%{gem_instdir}/test/

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.0.7.1-3
- 为 Magic 3.0 重建

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Apr 20 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.0.7.1-1
- 0.0.7.1

* Fri Jan 16 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.0.6-8
- F-22: Rebuild for ruby 2.2

* Fri Nov 14 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.0.6-7
- F-21 shoulda is now 3.5.0, fix test case

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 22 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.0.6-4
- Use minitest/autorun instead of minitest/unit

* Tue Apr 22 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.0.6-3
- F-21: rebuild for ruby 2.1 / rubygems 2.2

* Wed Sep 25 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.0.6-2
- Misc fix

* Fri Mar 22 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.0.6-1
- 0.0.6
- Support new ruby packaging guideline

* Sun Jan 06 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.0.5-1
- Initial package
