%global	gem_name	byebug

Name:		rubygem-%{gem_name}
Version:	6.0.2
Release:	2%{?dist}

Summary:	Ruby 2.0 fast debugger - base + CLI
License:	BSD

URL:		http://github.com/deivid-rodriguez/byebug
Source0:	https://rubygems.org/gems/%{gem_name}-%{version}.gem
# %%{SOURCE2} %%{name} %%{version} 
Source1:	rubygem-%{gem_name}-%{version}-full.tar.gz
Source2:	byebug-create-full-tarball.sh

BuildRequires:	rubygems-devel 
BuildRequires:	ruby-devel
# %%check
BuildRequires:	rubygem(minitest) >= 5
BuildRequires:	rubygem(columnize)
BuildRequires:	rubygem(mocha)
BuildRequires:	rubygem(simplecov)

%description
Byebug is a Ruby 2 debugger. It's implemented using the
Ruby 2 TracePoint C API for execution control and the Debug Inspector C API
for call stack navigation.  The core component provides support that
front-ends can build on. It provides breakpoint handling and bindings for
stack frames among other things and it comes with an easy to use command
line interface.


%package	doc
Summary:	Documentation for %{name}
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version} -a 1
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

# Relax columnize dependency
sed -i %{gem_name}.gemspec -e '\@columnize@s|= [0-9\.][0-9\.]*|>= 0.8.9|'

%build
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a .%{gem_extdir_mri}/{gem.build_complete,%{gem_name}/} %{buildroot}%{gem_extdir_mri}/
rm -rf %{buildroot}%{gem_instdir}/ext/

mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
	%{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x


%check
remove_fail_test() {
	filename=$1
	shift
	num=$#
	while [ $num -gt 0 ]
	do
		if [ ! -f ${filename}.orig ] ; then
			cp -p $filename ${filename}.orig
		fi
		sed -i $filename -e "\@def.*$1@s|^\(.*\)$|\1; skip \"Skip this\"|"
		shift
		num=$((num - 1))
	done
}

cp -a %{gem_name}-%{version}/{test,script} .%{gem_instdir}
pushd .%{gem_instdir}


# Once test all
ruby -I.:lib:ext script/minitest_runner.rb

%if 0
remove_fail_test test/commands/frame_test.rb \
	test_frame_minus_one_sets_frame_to_the_last_one

ruby -w -Ilib:ext test/test_helper.rb \
	$(ruby -e "puts Dir.glob('test/**/*_test.rb').join(' ')")
%endif

popd

%files
%dir	%{gem_instdir}
%license	%{gem_instdir}/LICENSE
%doc	%{gem_instdir}/CHANGELOG.md
%doc	%{gem_instdir}/CONTRIBUTING.md
%doc	%{gem_instdir}/GUIDE.md
%doc	%{gem_instdir}/README.md

%{_bindir}/byebug
%{gem_instdir}/bin

%{gem_libdir}/
%{gem_extdir_mri}/

%exclude	%{gem_cache}
%{gem_spec}

%files doc
%doc	%{gem_instdir}/CONTRIBUTING.md
%doc	%{gem_docdir}

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 6.0.2-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.0.2-1
- 6.0.2

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 19 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.0.0-1
- 5.0.0

* Fri Apr  3 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.0.5-1
- 4.0.5

* Sat Mar 28 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.0.4-1
- 4.0.4

* Fri Mar 20 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.0.3-1
- 4.0.3

* Tue Mar 17 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.0.2-1
- 4.0.2

* Sat Feb 07 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.5.1-4
- Remove simplecov

* Tue Feb 03 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.5.1-3
- A bit modification for %%check

* Tue Feb 03 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.5.1-2
- Make test suite exit with status

* Tue Feb 03 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.5.1-1
- Initial package
