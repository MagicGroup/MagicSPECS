# Generated from rttool-1.0.3.0.gem by gem2rpm -*- rpm-spec -*-
%global	gem_name	rttool

%if 0%{?fedora} >= 21
%global	gem_minitest	rubygem(minitest4)
%else
%global	gem_minitest	rubygem(minitest)
%endif

Name:		rubygem-%{gem_name}
Version:	1.0.3.0
Release:	8%{?dist}

Summary:	Converter from RT into various formats
# See rttool.en.rd
License:	Ruby
# raa is dead
#URL:		http://raa.ruby-lang.org/project/rttool/
URL:		https://github.com/genki/rttool
Source0:	https://rubygems.org/gems/%{gem_name}-%{version}.gem

BuildRequires:	ruby(release)
BuildRequires:	rubygems-devel
BuildRequires:	%gem_minitest
BuildRequires:	rubygem(test-unit)
BuildRequires:	rubygem(rdtool)
Requires:	ruby(release)
Requires:	ruby(rubygems)

BuildArch:	noarch
Provides:	rubygem(%{gem_name}) = %{version}-%{release}

%description
RT is a simple and human-readable table format.
RTtool is a converter from RT into various formats.
RT can be incorporated into RD.

%package	doc
Summary:	Documentation for %{name}
Group:	Documentation
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description doc
Documentation for %{name}

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

# Encoding
for f in \
	rttool.*.*
do
	iconv -f EUC-JP -t UTF-8 -o $f{.utf,}
	touch -r $f{,.utf}
	mv $f{.utf,}
done

# shebang
sed -i \
	-e '\@#![ \t]*/usr/bin/ruby@d' \
	lib/rt/*.rb

%build
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
	%{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

%check
pushd .%{gem_instdir}
chmod 0755 bin/rt2

export RUBYOPT="-I$(pwd)/lib"
export PATH=$(pwd)/bin:$PATH
ruby -Ilib:. -e 'gem "minitest", "<5" ; Dir.glob("test/test*.rb").each {|f| require f}'

popd

%files
%dir	%{gem_instdir}
%doc	%{gem_instdir}/ChangeLog
%doc	%{gem_instdir}/GPL
%doc %{gem_instdir}/rttool.*.html
%doc	%{gem_instdir}/rttool.*.rd

%{_bindir}/rdrt2
%{_bindir}/rt2
%{gem_instdir}/bin

%{gem_libdir}
%exclude	%{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/examples/
%exclude	%{gem_instdir}/test/

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 1.0.3.0-8
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.0.3.0-7
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.0.3.0-6
- 为 Magic 3.0 重建

* Tue Jun 23 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.0.3.0-5
- BR: rubygem(test-unit)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 12 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.0.3.0-3
- Force to use minitest ver4 for now

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Nov 15 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.0.3.0-1
- Initial package
