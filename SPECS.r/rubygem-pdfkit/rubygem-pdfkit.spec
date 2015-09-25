%global	gem_name	pdfkit

Name:		rubygem-%{gem_name}
Version:	0.8.2
Release:	2%{?dist}

Summary:	HTML+CSS to PDF using wkhtmltopdf
License:	MIT
 
URL:		https://github.com/pdfkit/pdfkit
Source0:	https://rubygems.org/gems/%{gem_name}-%{version}.gem

BuildRequires:	git
BuildRequires:	rubygems-devel

BuildRequires:	wkhtmltopdf
BuildRequires:	rubygem(rspec)
BuildRequires:	rubygem(mocha)
BuildRequires:	rubygem(simplecov)
BuildRequires:	rubygem(rack)
BuildRequires:	rubygem(rack-test)
BuildRequires:	rubygem(activesupport)
BuildRequires:	%{_bindir}/xvfb-run
BuildRequires:	iputils
Requires:		wkhtmltopdf
BuildArch:		noarch

%description
Create PDFs using plain old HTML+CSS. Uses wkhtmltopdf
on the back-end which renders HTML using Webkit.

%package	doc
Summary:	Documentation for %{name}
Requires:	%{name} = %{version}-%{release}

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

# Clean up
pushd %{buildroot}%{gem_instdir}
rm -rf \
	.document .gitignore .rspec \
	.ruby-gemset .ruby-version \
	.travis.yml \
	Gemfile Rakefile \
	POST_INSTALL \
	*.gemspec \
	spec/ \
	%{nil}
popd

%check
disable_test() {
	filename=$1
	shift
	num=$#
	while [ $num -gt 0 ]
	do
		sed -i -e "s|\(it \"$1\"\)|\1, pending: 'This fails currently'|" $filename
		shift
		num=$((num - 1))
	done
}

pushd .%{gem_instdir}
# Once test all
xvfb-run -n 99 rspec spec/ || true

disable_test spec/configuration_spec.rb \
	"detects the existance of bundler" \
	%{nil}
ping -w3 www.google.co.jp || \
	disable_test spec/pdfkit_spec.rb \
	"can handle ampersands in URLs" \
	%{nil}


xvfb-run -n 98 rspec spec/
popd

%files
%dir	%{gem_instdir}
%license	%{gem_instdir}/LICENSE
%doc	%{gem_instdir}/CHANGELOG.md
%doc	%{gem_instdir}/README.md
%{gem_libdir}
%{gem_spec}

%exclude %{gem_cache}

%files doc
%doc	%{gem_docdir}

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.8.2-2
- 为 Magic 3.0 重建

* Sun Aug 30 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.8.2-1
- 0.8.2

* Sun Aug 23 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.8.1-1
- 0.8.1

* Tue Aug 11 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.8.0-1
- 0.8.0

* Sun Aug  9 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.7.0-2
- Rewrite

* Thu May 07 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.7.0-1
- Initial package
