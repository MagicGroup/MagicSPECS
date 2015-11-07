%global	gem_name	power_assert

Name:		rubygem-%{gem_name}
Version:	0.2.4
Release:	102%{?dist}

Summary:	Power Assert for Ruby
License:	Ruby or BSD
URL:	https://github.com/k-tsj/power_assert
Source0:	https://rubygems.org/gems/%{gem_name}-%{version}.gem

BuildRequires:	rubygems-devel
BuildRequires:	rubygem(test-unit)

%if 0%{?fedora} < 21
Requires:	ruby(release)
Requires:	ruby(rubygems)
Provides:	rubygem(%{gem_name}) = %{version}
%endif

BuildArch:	noarch

%description
Power Assert for Ruby. Power Assert shows each value of variables and method
calls in the expression. It is useful for testing, providing which value
wasn't correct when the condition is not satisfied.

%package	doc
Summary:	Documentation for %{name}
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

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

# cleanup
pushd %{buildroot}%{gem_instdir}

rm -rf \
	.gitignore .travis.yml \
	Gemfile LEGAL \
	Rakefile \
	*gemspec \
	test/

popd

%check
pushd .%{gem_instdir}
ruby -Ilib:. \
	-e \
	'gem "test-unit"; Dir.glob("test/test*.rb").each {|f| require f}'
popd

%files
%dir	%{gem_instdir}
%license	%{gem_instdir}/BSDL
%license	%{gem_instdir}/COPYING
%doc	%{gem_instdir}/README.rdoc
%{gem_libdir}
%{gem_spec}

%exclude	%{gem_cache}

%files	doc
%doc	%{gem_docdir}

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.2.4-102
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.2.4-101
- 为 Magic 3.0 重建

* Wed Jul 22 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.2.4-100
- 0.2.4

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-101
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Mar  1 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.2.3-100
- 0.2.3

* Sun Dec 14 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.2.2-100
- Bump release massively (for ruby srpm)

* Tue Dec  2 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.2.2-2
- Misc cleanup

* Thu Nov 27 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.2.2-1
- 0.2.2
- Kill unneeded BR

* Sun Nov 16 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.2.1-1
- Initial package
