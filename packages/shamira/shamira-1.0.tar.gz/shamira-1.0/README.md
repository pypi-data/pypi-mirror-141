# Shamira #

Implements [Shamir's secret sharing algorithm](https://en.wikipedia.org/wiki/Shamir's_Secret_Sharing). Splits a string or a byte sequence byte-per-byte into _n_<255 shares, with any _k_ of them sufficient for reconstruction of the original input.

Outputs the shares as hexadecimal, Base32 or Base64 encoded strings.

## Installation ##

### From pip

Run `pip install shamira`.

### From the source
Can be run straight from the cloned repository by executing the package with `python -m shamira` or built with `python -m build` and installed with `pip install dist/shamira*.whl`.

## Usage

### As a CLI application

Run `shamira split ...` for splitting and `shamira join ...` for joining the shares back. Appending `--help` will show you the documentation.

### As a library

`from shamira import generate, generate_raw, reconstruct, reconstruct_raw`

`help(function)` will show the documentation. 

## Issue tracker
Please report your issues to https://trac.19x19.cz/shamira/report

## Performance ##

Being written in pure Python, the code is not especially fast. It is therefore recommended to split rather keys to encrypted files than the files themselves.

Benchmark results, as obtained by running `shamira benchmark`. All values mean _seconds per byte_ of the secret length:
<table>
    <tr>
        <th>k / n parameters</th>
        <th>Split</th>
        <th>Join</th>
    </tr>
    <tr>
        <td>2 / 3 (a Raspberry Pi 3)</td>
        <td>0.000142</td>
        <td>0.000448</td>
    </tr>
    <tr>
        <td>2 / 3 (a laptop)</td>
        <td>7.88e-06</td>
        <td>4.28e-05</td>
    </tr>
    <tr>
        <td>254 / 254 (a Raspberry Pi 3)</td>
        <td>0.0268</td>
        <td>0.0287</td>
    </tr>
    <tr>
        <td>254 / 254 (a laptop)</td>
        <td>0.00183</td>
        <td>0.00156</td>
    </tr>
</table>

## License ##

The code is licensed under GNU GPL v3. If this doesn't fit your needs, reach me and we can negotiate relicensing.
